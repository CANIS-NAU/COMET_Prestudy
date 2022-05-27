# imports
import argparse
import pandas as pd

from BaseScraper import Scraper
import requests


# Scraper definitions
class OCellIDScraper(Scraper):
    """Scraper object that specifically handles the OpenCellID forums (community.opencellid.org/)

    This Scraper object will make use of Discourse's REST API for fetching JSON files from the server
    This will make use of special URL syntax that will grab the required data from each search query as
    well as each selected post.

    **Getting all replies from within in a selected topic (including original post):**
    ``https://community.opencellid.org/t/{**topic_id**}.json?print=true``
    """

    def __init__(self, base_url: str, keywords_file: str, driver: str):
        super().__init__(base_url, keywords_file, driver)

    def _collect_page_metadata(self, post_json) -> dict:
        """When the desired page (a post containing all wanted data) is loaded,
        Identify the fields that need to be populated (within this object) and
        extract the data by whatever means necessary. Place the values into a dictionary
        that follows the format: { "field-name": "extracted-value", ... }

        Helper functions can be declared inside this method in order to keep things
        organized, but its no biggie.

        Parameters
        ----------
        post_metadata_json : dict
            The JSON-formatted output of the specific post's page.

        Returns
        -------
        dict
            Filtered output data that will be used to populate a Post object

        """

        OG_POST_INDEX = 0

        def get_title() -> str:
            (title,) = list(post_json.values())
            title = title[OG_POST_INDEX]["topic_slug"]
            return title

        def get_date() -> str:
            (date,) = list(post_json.values())
            date = date[OG_POST_INDEX]["created_at"]

            return date

        def get_responses() -> list[str]:
            (responses,) = list(post_json.values())
            responses = responses[1:]
            filtered_responses = {
                item["id"]: {
                    "username": item["username"],
                    "content": item["cooked"],
                    "date": item["created_at"],
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
            content = content[OG_POST_INDEX]["cooked"]
            return content

        def get_post_id() -> str:
            (id,) = post_json.keys()
            return id

        # convert results of the above functions into the wanted dictionary format
        metadata_dict = {
            "post_id": get_post_id(),
            "title": get_title(),
            "author": get_author(),
            "date": get_date(),
            "content": get_post_content(),
            "replies": get_responses()
        }

        return metadata_dict

    def _find_posts(self, search_json) -> list[int] | None:
        """Provided a list of posts after a search query, parse the search JSON
        and return the IDs of all the resulting posts from the search.

        Parameters
        ----------
        search_json : dict
            The JSON result returned after conducting a :func:`~OCellIDScraper.search()` operation

        Returns
        -------
        list[str]
            A list of URLs for each identified post
        """

        if "topics" in search_json:
            posts = [topic["id"] for topic in search_json["topics"]]
            return posts
        else:
            return None

    def goto(self, url):
        """For this website, goto() will make a get request to the specified website
        and return the response data as a result

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

    def _new_post(self, post_output):
        """With the help of the _collect_page_metadata function,
        gather the post data, then place the data into the appropriate
        fields within a respective Post subclass

        Parameters
        ----------
        keyword : str
            The search term that was used to obtain this post as a result
        post_json : dict
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

        # iterate through keywords
        for keyword in self.keywords:

            # search keyword
            print("[INFO] Searching With Keyword: {}".format(keyword))
            search_json = self.search(keyword)

            # Find post results from keyword search
            search_result_ids = self._find_posts(search_json)

            # if posts exist, get them and store in self.posts
            if search_result_ids:

                print("[INFO] {} results found for keyword: {}".format(len(search_result_ids), keyword))

                # for posts in list of post urls
                for iter, topic_id in enumerate(search_result_ids):

                    print("[INFO] Scraping post {}/{}".format(iter+1, len(search_result_ids)))

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
                print(f"[INFO] No results for keyword: {keyword}")

        # convert posts dictionary into a DataFrame
        print("[INFO] Removing Duplicates")
        self.posts = pd.DataFrame(self.posts).drop_duplicates(subset=['post_id'])


    def search(self, search_term: str):
        """Using the Discourse URL API, this function will send a get request to the
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

    parser = argparse.ArgumentParser(description="Script for scraping MLab google groups discussion forum")
    parser.add_argument('keywords_dir', help='path to the file where all keywords are listed', type=str)
    parser.add_argument('data_out', type=str, help="path+filename of the outputted tsv/csv file")
    parser.add_argument('--driver', '-d', type=str, help="The browser you plan to use for scraping. Defaults to Google Chrome.", default='chrome', choices=['chrome', 'firefox', 'opera', 'safari'])


    args = parser.parse_args()

    google_groups_scraper = OCellIDScraper(default_group_url, args.keywords_dir, args.driver)
    google_groups_scraper.scrape()

    google_groups_scraper.flush_posts(args.data_out)

if __name__ == '__main__':
    main()