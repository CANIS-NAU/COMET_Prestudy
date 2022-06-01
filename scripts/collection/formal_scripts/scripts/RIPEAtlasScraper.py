#!/usr/bin/env python3

import argparse
from datetime import datetime

import pandas as pd
from dateutil import parser
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.support.wait import WebDriverWait

from BaseScraper import Scraper


class RipeAtlasScraper(Scraper):
    def __init__(
        self,
        base_url: str,
        driver: str | None,
        age_threshold: str | None,
    ):
        # for the purposes of formal scrapers, I will set all keyword directories to None
        super().__init__(base_url, None, driver, age_threshold)

    def _collect_page_metadata(self, index) -> dict:

        # Create helper functions to handle each data task, Examples could include:
        def get_post_title() -> str:
            title_element = self.driver.find_element(
                By.XPATH, "//h4[@class='no-margin-top']"
            ).text
            return title_element

        def get_post_date() -> datetime:
            date_element = self.driver.find_element(
                By.XPATH, "//p[@class='messagedate smallText']"
            ).text
            date_as_datetime = parser.parse(date_element, ignoretz=True)
            return date_as_datetime

        def get_post_author() -> str:
            post_author_element = self.driver.find_element(
                By.XPATH, "//p[@class='username'][1]"
            ).text
            return post_author_element

        def get_post_content() -> str:
            post_content_element = self.driver.find_element(
                By.XPATH, "(//pre[@class='padding'])[1]"
            ).text
            return post_content_element

        def get_responses():
            def get_response_author(reply_element) -> str:
                author_element = reply_element.find_element(
                    By.XPATH, ".//p[@class='username']"
                ).text
                return author_element

            def get_response_date(reply_element) -> datetime:
                date_element = reply_element.find_element(
                    By.XPATH, ".//p[@class='messagedate smallText']"
                ).text
                return parser.parse(date_element)

            # TODO - clean out previous response text (like email)
            def get_response_content(reply_element) -> str:
                response_content_element = reply_element.find_element(
                    By.XPATH, ".//pre[@class='padding']"
                ).text
                return response_content_element

            temp_resp_container = {}

            response_element_arr = self.driver.find_elements(
                By.XPATH, "//div[@id='messages']/div"
            )[1:]

            for index, response in enumerate(response_element_arr):
                resp_author = get_response_author(response)
                resp_date = get_response_date(response)
                resp_content = get_response_content(response)

                temp_resp_container[index] = {
                    "username": resp_author,
                    "date_epoch": resp_date.timestamp(),
                    "date_ymd": resp_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "response_content": resp_content,
                }

            return temp_resp_container

        # use above helpers to assign variables
        # title = get_post_title()
        # post_Date = get_post_date()
        # ...
        title = get_post_title()
        author = get_post_author()
        date = get_post_date()
        content = get_post_content()
        replies = get_responses()

        # use the above variables to create a dictionary
        # structure and return it
        return {
            "post_id": index,
            "title": title,
            "author": author,
            "date_epoch": date.timestamp(),
            "date_ymd": date.strftime("%Y-%m-%d %H:%M:%S"),
            "content": content,
            "responses": replies,
        }

    def _find_posts(self) -> list[str]:

        # temp list to store each identified post link
        link_list = []

        # Do-while loop - while there is a next page
        while True:

            # with wait, get array of webelements that correspond to all post items
            post_elements = WebDriverWait(self.driver, 3).until(
                presence_of_all_elements_located(
                    (
                        By.XPATH,
                        "//div[@id='messages']/div[@class='grey-border-bottom padding']",
                    )
                )
            )

            # for posts in element array
            for post in post_elements:

                # grab href/url attribute
                post_href_attribute = post.find_element(
                    By.XPATH, "./p[1]/a"
                ).get_attribute("href")

                # grab date attribute as str (datetime)
                post_date_attribute = post.find_element(By.XPATH, "./p[2]/a").text
                post_bump_date = parser.parse(
                    post_date_attribute, ignoretz=True
                )  # datetime.strptime(post_date_attribute, '%Y-%m-%d %H:%M:%S %Z')

                # if post date within threshold
                if post_bump_date >= self.age_threshold:
                    # append url to temp array above
                    link_list.append(post_href_attribute)

                else:
                    return link_list

            self._next_page()

    def _next_page(self):
        next_page_button = WebDriverWait(self.driver, 3).until(
            visibility_of_element_located(
                (By.XPATH, "//a[@class='btn btn-default pull-right']")
            )
        )
        cookie_popup = self.driver.find_elements(
            By.XPATH, "//div[@id='cookiepopup']//i"
        )

        if any(cookie_popup):
            cookie_popup[-1].click()

        try:
            next_page_button.click()

        except Exception as e:
            raise e

    def _new_post(self, index: int):

        # call _collect_page_metadata() to create dictionary with page data
        # NOTE - index is for creating post IDs, which dont exist by default
        metadata = self._collect_page_metadata(index)

        # append newly created dictionary to self.posts arr for storage
        self.posts.append(metadata)

    def scrape(self):

        # wait a bit before starting scraping
        self.driver.implicitly_wait(1)

        # go to base url
        self.goto(self.base_url)

        # find post urls for all pages (until next_page returns false)
        found_post_urls = self._find_posts()

        # if url's are found (there should be)
        if any(found_post_urls):

            # for each url identified
            for index, url in enumerate(found_post_urls):

                # tell user the progress of scraping
                print(
                    "[INFO] Scraping post {}/{}".format(index + 1, len(found_post_urls))
                )

                # Go to post url
                self.goto(url)

                # create new post with that data (append to self.posts)
                self._new_post(index)

        # else
        else:
            # tell the user that no posts were found
            print("[WARNING] No posts found for base URL {}".format(self.base_url))

        # convert dictionary into pandas dataframe
        self.posts = pd.DataFrame(self.posts)

        # close the WebDriver connection
        self.close()


def main():

    ripe_atlas_forum_url = "https://www.ripe.net/participate/mail/forum/ripe-atlas"
    ripe_atlas_cooperation_forum_url = (
        "https://www.ripe.net/participate/mail/forum/cooperation-wg"
    )

    parser = argparse.ArgumentParser(
        description="Scrape the RIPE Atlas community forums for data"
    )

    parser.add_argument(
        "data_out",
        type=str,
        help="The output directory+filename of the resulting tsv file",
    )

    parser.add_argument(
        "--age_threshold",
        "-a",
        default=None,
        help="Get most recently commented posts up to specified date (inclusive); Format: MM/YYYY, None == get all posts",
        type=str,
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

    # TODO - determine which forums specifically to scrape
    ripe_scraper = RipeAtlasScraper(
        ripe_atlas_forum_url, driver=args.driver, age_threshold=args.age_threshold
    )

    ripe_scraper.scrape()

    ripe_scraper.flush_posts(args.data_out)


if __name__ == "__main__":
    main()
