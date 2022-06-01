#!/usr/bin/env python3

# imports
import argparse
from datetime import datetime

import pandas as pd
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.support.wait import WebDriverWait

from BaseScraper import Scraper


class GoogleGroupsScraper(Scraper):

    ########## Public Methods ##########
    def __init__(self, site_url: str, driver: str, age_threshold: str):
        super().__init__(site_url, None, driver, age_threshold=age_threshold)

    def _next_page(self) -> bool:
        """For Google Groups, this function handles moving to the
        next page to gather more data from subsequent 'paginated' pages

        Returns
        -------
        bool
            If True, there are still pages that need to be grabbed, continue
            the operation. If False, we have reached the end of the pages, stop
            the operation.
        """

        from selenium.webdriver.common.action_chains import ActionChains

        action_chain = ActionChains(self.driver)

        # identify 'next page' button
        next_page_button = WebDriverWait(self.driver, 10).until(
            presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'div[aria-label="Next page"]')
            )
        )[-1]

        # if next page button is available
        tab_index = int(next_page_button.get_attribute("tabindex"))
        is_visible = tab_index == 0
        if is_visible:
            for attempt in range(10):
                # attempt to click the button
                try:
                    action_chain.move_to_element_with_offset(next_page_button, 1, 1)
                    action_chain.click()
                    action_chain.perform()
                    self.driver.implicitly_wait(1)

                except Exception as e:
                    # if there is an exception, wait some time and try again; Stops after 10 tries
                    print("[WARNING] {} Trying again ({})...".format(e, attempt + 1))
                    self.driver.implicitly_wait(2)
                    continue

                else:
                    return True

            raise Exception(e)

        # else
        else:
            # let the user know that this is the last page of the website
            print("[INFO] Last page reached...")
            return False

    def scrape(self):

        self.driver.implicitly_wait(1)

        self.goto(self.base_url)

        # collect post urls from root directory
        post_urls = self._find_posts()

        # if results exist
        if post_urls:

            # store item into the Scraper.posts dictionary
            for iter, post in enumerate(post_urls):
                print("[INFO] Scraping Post {}/{}".format(iter + 1, len(post_urls)))
                self.goto(post)
                self._new_post(iter)

        # else
        else:
            # tell the user that there were no results for this keyword
            print(f"[WARNING] No results...")

        self.posts = pd.DataFrame(self.posts)
        self.close()

    def search(self, search_term: str):
        """For Google Groups, navigate to the search bar and
        enter the search terms. Then search the group and return
        the resulting page

        Args:
            search_term (str): keyword/query that you wish to enter into the search bar
        """

        # format string to make manual get request
        get_syntax = "search?q="
        get_space_char = "%20"
        query = get_syntax + search_term.replace(" ", get_space_char)

        # go to the page with newly formatted request string for url
        self.goto(self.base_url + "/" + query)

    ########## Private Methods ##########
    def _find_posts(self) -> list[str]:
        """Identify new posts on current page.

        In the case of Google Groups, all posts are all filtered <a> tags
        containing '/c/' located in the root page

        Returns:
            list[str]: list of urls for all identified posts located in the group
        """

        parsed_links = []

        print("[INFO] Identifying posts within {}".format(self.base_url))

        # emulation of a do-while loop
        while True:

            # grabs all of the clickable links to each post (no duplicates) and returns array of links
            if any(self.driver.find_elements(By.XPATH, "//div[@role='main']/h1")):
                return None

            else:
                posts = WebDriverWait(self.driver, 5).until(
                    presence_of_all_elements_located(
                        (By.XPATH, "((//div[@role='row'])[position() > 1])")
                    )
                )

                for post in posts:
                    post_link = post.find_element(
                        By.XPATH, "./div/span[3]/div/a"
                    )  # self.driver.find_elements(By.XPATH, "((//div[@role='row'])[position() > 1])/div/span/div/a[contains(@href, '/c/')]")
                    date_str_from_element = post.find_element(
                        By.XPATH, ".//span[4]/div/div/div[1]"
                    ).text
                    post_date = datetime.strptime(
                        date_str_from_element,
                        (
                            "%m/%d/%y"
                            if is_mdy_format(date_str_from_element)
                            else "%b %d"
                        ),
                    )
                    try:
                        url = post_link.get_attribute("href")
                    except StaleElementReferenceException:
                        self.driver.refresh()
                        print(
                            "\n\nPOST_REFRESH"
                            + post_link.get_attribute("outerHTML")
                            + "END_POST_REFRESH\n\n"
                        )
                        continue

                    else:
                        if (
                            post_date >= self.age_threshold or post_date.year == 1900
                        ):  # 1900 is the default when no year is provided
                            parsed_links.append(url)

            if not self._next_page():
                break

        return parsed_links

    def _collect_page_metadata(self, index) -> dict:
        """When the desired page (a post containing all wanted data) is loaded,
        Identify the fields that need to be populated (within this object) and
        extract the data by whatever means necessary. Place the values into a dictionary
        that follows the format: { "field-name": "extracted-value", ... }
        """

        self._expand_all_posts()

        title = self.driver.title.lower().replace(" ", "-")
        author = self._get_post_author()
        content = self._get_content()
        replies = self._get_responses()
        date = self._get_post_date()

        post_id = index
        return {
            "post_id": post_id,
            "title": title,
            "date_epoch": date.timestamp(),
            "date_ymd": date.strftime("%Y-%m-%d %H:%M:%S"),
            # "media"
            "author": author,
            "content": content,
            "replies": replies,
        }

    def _expand_all_posts(self):
        """Helper function just for Google Groups...
        From within the google groups page, make sure that all posts are expanded
        by clicking the 'expand all' button on the page.
        """

        # identify the expand all button on the page
        expand_button = self.driver.find_elements(
            By.XPATH, "//div[@role='button' and @aria-label='Expand all']"
        )

        if any(expand_button):

            try:
                expand_button.pop().click()

            except Exception:
                pass

    def _new_post(self, index):
        """After collecting all post data, use this function to
        organize and place the data in their appropriate fields
        within the class.
        """
        metadata = self._collect_page_metadata(index)
        self.posts.append(metadata)

    def _get_post_date(self) -> datetime:

        date_item = self.driver.find_element(
            By.XPATH, "((//section[1])//div//span)[2]"
        ).text

        date_as_datetime_format = datetime.strptime(date_item, "%b %d, %Y, %I:%M:%S %p")

        return date_as_datetime_format

    def _get_content(self) -> str:
        """Helper function just for Google Groups...

        Identifies which page elements are the **Original Post Body Content**
        and returns the post text.

        Returns
        -------
        str
            Text content from the original post
        """
        # find the part of the post webpage that contains <html-blob> tag
        value = self.driver.find_element(
            By.XPATH, "(//div[@role='region' ])[1]"
        ).text.replace("\n", " ")
        return value

    def _get_post_author(self) -> str:
        """Helper function just for Google Groups...

        Identifies which page element(s) contain **Author Name Content**
        and returns the original post's author's name as a string

        Returns
        -------
        str
            Post author's name
        """
        value = self.driver.find_elements(By.XPATH, "(//h3)")
        if value[0]:
            return value[0].text
        else:
            print("what the heck just happened")

    # NOTE: Side-effect, if a single person replies multiple times in the same post, all reply strings
    # are attached to the same single author in the dictionary
    def _get_responses(self) -> dict[str:str]:
        """Helper function just for Google Groups...

        Identifies which page elements contain **Response Content** and
        returns a dictionary of strings with the following format:

        ``{author:response, author2:response2, author3:response3, ...}``

        Returns
        -------
        dict
            Dictionary with grouped reply author and reply body content
        """

        value = {}

        # find lists of authors and their replies attempt 10 tries
        try:
            author_str = WebDriverWait(self.driver, 2).until(
                presence_of_all_elements_located((By.XPATH, "(//h3)[position()>1]"))
            )
            response_str = WebDriverWait(self.driver, 2).until(
                presence_of_all_elements_located(
                    (By.XPATH, "(//div[@role='region' ])[position()>1]")
                )
            )
            response_dates = WebDriverWait(self.driver, 2).until(
                presence_of_all_elements_located(
                    (
                        By.XPATH,
                        "((//div[@role='region' ])[position()>1])/../div[1]/div[1]/div[2]/span[1]",
                    )
                )
            )

            # stitch together both lists into dictionary with structure {author:response}
            if len(author_str) == len(response_str) == len(response_dates):
                for index in range(len(author_str)):
                    value[index] = {
                        "username": author_str[index].text,
                        "response_date": response_dates[index].text,
                        "response_content": response_str[index].text.replace("\n", " "),
                    }
        except TimeoutException:
            print("[WARNING] Likely no responses here, Continuing...")
            pass

        else:
            raise Exception(
                "[ERROR] Response Data Mismatch...\n\nResponse Values\nAuthorLen:{}\nReplyDateLen:{}\nReplyContentLen:{}".format(
                    len(author_str), len(response_dates), len(response_str)
                )
            )

        finally:
            return value


def is_mdy_format(date_text):
    """Helper that determines if the param string
    is in the desired '%m/%d/%y' format
    """
    try:
        datetime.strptime(date_text, "%m/%d/%y")
        return True
    except ValueError:
        return False


# lastly, we implement a main method to make this script executable
def main():
    default_group_url = "https://groups.google.com/a/measurementlab.net/g/discuss"

    parser = argparse.ArgumentParser(
        description="Script for scraping MLab google groups discussion forum"
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
    parser.add_argument(
        "--driver",
        "-d",
        type=str,
        help="The browser you plan to use for scraping. Defaults to Google Chrome.",
        default="chrome",
        choices=["chrome", "firefox", "opera", "safari"],
    )

    args = parser.parse_args()

    google_groups_scraper = GoogleGroupsScraper(
        default_group_url, args.driver, args.age_threshold
    )
    google_groups_scraper.scrape()

    google_groups_scraper.flush_posts(args.data_out)


if __name__ == "__main__":
    main()
