#!/usr/bin/env python3

# imports
import argparse
from datetime import datetime
from html.parser import HTMLParser
from io import StringIO

import pandas as pd
import requests

from BaseScraper import Scraper


class MLStripper(HTMLParser):
    """Copied from stackoverflow :P

    Helps strip unwanted HTML characters from
    content text.

    """

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


# Scraper definitions
class OCellIDScraper(Scraper):
    """Scraper object that specifically handles the OpenCellID forums (community.opencellid.org/)

    This Scraper object will make use of Discourse's REST API for fetching JSON files from the server
    This will make use of special URL syntax that will grab the required data from each search query as
    well as each selected post.

    **Getting all replies from within in a selected topic (including original post):**
    ``https://community.opencellid.org/t/{**topic_id**}.json?print=true``
    """

    def __init__(self, base_url: str, driver: str, age_threshold: str):
        super().__init__(base_url, None, driver, age_threshold=age_threshold)

    def _collect_page_metadata(self, post_json) -> dict:
        """When the desired page (a post containing all wanted data) is loaded,
        Identify the fields that need to be populated and
        extract the data by whatever means necessary. Place the values into a dictionary
        that follows the format: { "field-name": "extracted-value", ... }

        Helper functions can be declared inside this method in order to keep things
        organized, but its no biggie.

        Parameters
        ----------
        post_json : dict
            The JSON-formatted output of the specific post's page.

        Returns
        -------
        dict
            Filtered output data that will be used to populate the self.posts list

        """

        OG_POST_INDEX = 0

        def get_title() -> str:
            (title,) = list(post_json.values())
            title = title[OG_POST_INDEX]["topic_slug"]
            return title

        def get_date() -> datetime:
            (date,) = list(post_json.values())
            date = datetime.strptime(
                date[OG_POST_INDEX]["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )

            return date

        def get_responses() -> list[str]:
            (responses,) = list(post_json.values())
            responses = responses[1:]
            filtered_responses = {
                item["id"]: {
                    "username": item["username"],
                    "date_epoch": datetime.strptime(
                        item["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    ).timestamp(),
                    "date_ymd": datetime.strptime(
                        item["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                    "content": strip_tags(item["cooked"]),
                }
                for item in responses
            }
            return filtered_responses

        def get_author() -> str:
            (author,) = list(post_json.values())
            author = author[OG_POST_INDEX]["username"]
            return author

        def get_post_content() -> str:
            (content,) = list(post_json.values())
            content = strip_tags(content[OG_POST_INDEX]["cooked"].replace("\n", " "))
            return content

        def get_post_id() -> str:
            (id,) = post_json.keys()
            return id

        date = get_date()

        # convert results of the above functions into the wanted dictionary format
        metadata_dict = {
            "post_id": get_post_id(),
            "title": get_title(),
            "author": get_author(),
            "date_epoch": date.timestamp(),
            "date_ymd": date.strftime("%Y-%m-%d %H:%M:%S"),
            "content": get_post_content().replace('\t', ' '),
            "replies": get_responses(),
        }

        return metadata_dict

    def _find_posts(self) -> list[int] | None:
        """Parse and return the IDs of all resulting posts.

        Returns
        -------
        list[str]
            A list of IDs for each identified post
        """

        topic_list = []
        loop_index = 0
        page_url_str = "page="
        root_json = self.goto(f"{self.base_url}/top.json")

        while self.page_has_topics(root_json):
            posts = [
                topic["id"]
                for topic in root_json["topic_list"]["topics"]
                if datetime.strptime(
                    topic["last_posted_at"]
                    if topic["last_posted_at"]
                    else topic["created_at"],
                    "%Y-%m-%dT%H:%M:%S.%fZ",
                )
                >= self.age_threshold
            ]
            topic_list += posts
            loop_index += 1

            full_query_str = "{}?{}{}".format(
                self.base_url + "/" + "top.json", page_url_str, loop_index
            )
            root_json = self.goto(full_query_str)

        return topic_list

    def goto(self, url):
        """For this website, goto() will make a get request to the specified website
        and return the response JSON as a result

        Parameters
        ----------
        url : str
            The url of the website data that is required

        Returns
        -------
        dict
            JSON data from the requested page
        """
        json_return = requests.get(url).json()
        return json_return

    def page_has_topics(self, page_json) -> bool:
        """Boolean checker, alerts if there is a non-zero amount of posts
        as a result of a GET request.

        Parameters
        ----------
        page_json : dict
            The resulting JSON data as a result of a GET request ( ie. goto() )

        Returns
        -------
        bool
            True if >= 1 posts exist, False otherwise
        """
        if any(page_json["topic_list"]["topics"]):
            return True

        return False

    def _new_post(self, post_output):
        """**Abstraction** With the help of the _collect_page_metadata function,
        gather the post data, then place into the self.posts dictionary

        Parameters
        ----------
        post_output : dict
            The JSON data structure of a post on the website
        """
        metadata = self._collect_page_metadata(post_output)
        self.posts.append(metadata)

    def scrape(self):
        def get_chunks(target_list: list, chunk_size: int):
            """Create a 2D array with sub-arrays of size 'chunk_size'

            Parameters
            ----------
            target_list : list
                List that will be divided into sub-lists of size 'chunk_size'
            chunk_size : int
                the maximum length of a sub-array

            Yields
            ------
            list
                list of divided list elements the length of 'chunk_size'
            """
            for index in range(0, len(target_list), chunk_size):
                yield target_list[index : index + chunk_size]

        # Find post results from keyword search
        topic_ids = self._find_posts()

        # if posts exist, get them and store in self.posts
        if topic_ids:

            print("[INFO] {} topics found...".format(len(topic_ids)))

            # for posts in list of post urls
            for iter, topic_id in enumerate(topic_ids):

                print("[INFO] Scraping topic {}/{}".format(iter + 1, len(topic_ids)))

                # get post data in JSON format
                post_json = self.goto(f"{self.base_url}/t/{topic_id}.json")

                # get all post ids within this topic (converted to the needed url snippet format "post_ids[]={{id_num}}")
                all_post_ids_as_url_snippet = [
                    f"post_ids[]={post_id}"
                    for post_id in post_json["post_stream"]["stream"]
                ]

                # for each size-20 chunk of ID numbers
                dict_structure = {}
                for chunk in get_chunks(all_post_ids_as_url_snippet, 20):

                    # generate proper url string with the 20 ID numbers
                    # format: "/t/{{topic_id}}/posts.json?post_ids[]={{post_id1}}&post_ids[]={{post_id2}}..."
                    post_url_chunk = "{0}/t/{1}/posts.json?{2}".format(
                        self.base_url, topic_id, "&".join(chunk)
                    )

                    # grab the JSON file for those grouped 20 posts; append the wanted data into an array of dictionaries
                    collected_json = requests.get(post_url_chunk).json()
                    posts_arr = collected_json["post_stream"]["posts"]
                    if topic_id not in dict_structure:
                        dict_structure[topic_id] = posts_arr
                    else:
                        dict_structure[topic_id] += posts_arr

                # create new Post object with page metadata
                self._new_post(dict_structure)

        # else (no posts found)
        else:
            # alert the user that no posts were found with the specified keyword
            print("[INFO] No results...")

        # convert posts dictionary into a DataFrame
        self.posts = pd.DataFrame(self.posts)

    def search(self, search_term: str):
        """**Depricated: Not Needed for Formal Scrapers** Using the Discourse URL API, this function will send a get request to the
        OpenCellID forum website, and return a JSON document with the post IDs from
        the resulting query. This JSON document can then be returned and parsed based on
        what data is required.

        **Getting all posts as a result of a keyword search:**
        ``https://community.opencellid.org/search.json?q={**keyword**}``

        Parameters
        ----------
        search_term : str
            The keyword/search-term you wish to query the website for
        """

        open_cell_id_query_url = (
            self.base_url + "search.json?q=" + search_term.replace(" ", "%20")
        )
        search_json = requests.get(open_cell_id_query_url).json()
        return search_json


def main():
    default_group_url = "https://community.opencellid.org/"

    parser = argparse.ArgumentParser(
        description="Script for scraping OpenCellID discussion forum"
    )

    parser.add_argument(
        "data_out", type=str, help="path+filename of the outputted tsv/csv file"
    )

    parser.add_argument(
        "--age_threshold",
        "-a",
        type=str,
        default=None,
        help="Get most recently commented posts up to specified date (inclusive); Format: MM/YYYY, None == get all posts",
    )

    args = parser.parse_args()

    ocell_id_scrape = OCellIDScraper(default_group_url, None, args.age_threshold)
    ocell_id_scrape.scrape()

    ocell_id_scrape.flush_posts(args.data_out)


if __name__ == "__main__":
    main()
