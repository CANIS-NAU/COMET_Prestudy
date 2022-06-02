#!/usr/bin/env python3

import argparse
from datetime import datetime
from time import sleep

import pandas as pd
from dateutil import parser
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions, wait

from BaseScraper import Scraper


class FCCDisqusScraper(Scraper):
    """For this scraper, we're going to have to combine the results of multiple
    different sources. The post sources are located within the FCC Blog itself

    Responses to the blog posts will be scraped from the FCC's Disqus page.
    """

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

        # get post title
        def get_post_title():
            post_title_element = self.driver.find_element(
                By.XPATH,
                "//h2[@class='discussion-title text-brand link-default-hover']",
            ).text
            return post_title_element

        # get post date
        def get_post_dates() -> tuple:
            raise NotImplementedError

        # get post author
        def get_post_author() -> str:
            raise NotImplementedError

        # get post content
        def get_post_content() -> str:
            raise NotImplementedError

        # get responses
        def get_responses() -> dict:

            # get response author
            def get_response_author() -> str:
                raise NotImplementedError

            # get response date
            def get_response_date() -> tuple:
                raise NotImplementedError

            # get response content
            def get_response_content() -> str:
                raise NotImplementedError

            # temporary response container
            temp_resp_container = {}

            # get array of all response WebDriver Elements
            response_elements = wait.WebDriverWait(self.driver, 3).until(
                expected_conditions.presence_of_all_elements_located(
                    (By.XPATH, "//li[@class='post']")
                )
            )

            # for response in array of response elements
            for index, response in enumerate(response_elements):

                # create structured response dictionary with ID as primary key
                resp_author = get_response_author(response)
                resp_epoch, resp_date = get_response_date(response)
                resp_content = get_response_content(response)

                # append this structure to temporary response container
                temp_resp_container[index] = {
                    "username": resp_author,
                    "date_epoch": resp_epoch,
                    "date_ymd": resp_date,
                    "response_content": resp_content.replace("\n", " "),
                }

            # return remporary response container
            return temp_resp_container

        # create structured post dictionary with ID as primary key
        title = get_post_title()
        author = get_post_author()
        date_epoch, date = get_post_dates()
        content = get_post_content()
        responses = get_responses()

        # return structured post data dictionary
        return {
            "post_id": index,
            "title": title,
            "author": author,
            "date_epoch": date_epoch,
            "date_ymd": date,
            "content": content,
            "responses": responses,
        }

    def _find_posts(self) -> list[str]:

        # temp list to store each identified post link
        disqus_link_list = []

        # use next-page method to load all posts
        self._next_page()

        # collect all loaded posts
        post_elements = wait.WebDriverWait(self.driver, 3).until(
            expected_conditions.presence_of_all_elements_located(
                (By.XPATH, "//div[@class='cards']/div")
            )
        )

        # for post in posts
        for post in post_elements:
            pass

            # get post link attribute

            # go to post on FCC website

            # get post date element from FCC website

            # if date within date range (Now -> X)

                # extract FCC.gov redirect url

                # append to temp list

            # else break

        # return temp list of urls
        raise NotImplementedError

    def _new_post(self, keyword: str):
        raise NotImplementedError

    def _next_page(self) -> None:
        """Scrolls page all the way down until all content is loaded

        Thx Kylie :)

        """
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def _post_url_sanitizer(self, url: str):
        """In more recent Disqus posts by the FCC,
        the URL's to the main post content are corrupted
        with unneccesary strings that link to Drupal, and
        even then, just don't connect to the right address.
        This removes the unneccessary strings from those urls
        if necessary.

        Ex.
            Bad:
            ``https://drupal7admin.fcc.gov/news-events/blog/2020/12/23/grand-finale``

            Good:
            ``https://fcc.gov/news-events/blog/2020/12/23/grand-finale``
        """

        str_to_remove = "drupal7admin."
        if str_to_remove in url:
            url.replace(str_to_remove, "")

        return url

    def scrape(self):

        # wait a bit before starting scraping (implicit wait)

        # go to base url

        # find post urls for all pages (until posts are outside of date range)

        # if url's are found (there should be)

            # for each url identified

                # tell the user the progress of scraping

                # go to post url

                # Identify wanted page metadata and create new post structure

        # else
            # tell the user that no posts were found

        
        # convert generated dictionary structure to pandas DataFrame

        # close the WebDriver Connection
        raise NotImplementedError
        

def main():
    parser = argparse.ArgumentParser(
        description="Scrape the FCC Disqus page for conversation data"
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

    fcc_url = "https://disqus.com/home/forum/fccdotgov/"

    args = parser.parse_args()

    disqus_scraper = FCCDisqusScraper(fcc_url, args.driver, args.age_threshold)

    disqus_scraper.scrape()

    disqus_scraper.flush_posts(args.data_out)
