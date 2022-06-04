#!/usr/bin/env python3

import argparse
from datetime import datetime
from time import sleep

import pandas as pd
from dateutil import parser
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions, wait
from selenium.webdriver.remote.webelement import WebElement

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

        self.wait = wait.WebDriverWait(self.driver, 5)

    def _collect_page_metadata(self, index: str, post_data: dict) -> dict:

        # Create helper functions to handle each data task

        # get post date
        def get_post_dates(date_str: str) -> tuple:
            date = parser.parse(date_str)
            return date.timestamp(), date.strftime("%Y-%m-%d %H:%M:%S")

        # get responses
        def get_responses() -> dict:

            # get response author
            def get_response_author(resp_element: WebElement) -> str:
                author_element = resp_element.find_element(
                    By.XPATH, './/span[@class="author publisher-anchor-color"]/a'
                ).text
                return author_element

            # get response date
            def get_response_date(resp_element: WebElement) -> tuple:
                date_element = resp_element.find_element(
                    By.XPATH, ".//a[@class='time-ago']"
                ).get_attribute("title")
                return get_post_dates(date_element)

            # get response content
            def get_response_content(resp_element: WebElement) -> str:
                content_element = resp_element.find_element(
                    By.XPATH, './/div[@class="post-message "]//p'
                ).text
                return content_element

            # temporary response container
            temp_resp_container = {}

            # get array of all response WebDriver Elements
            self.wait.until(
                expected_conditions.frame_to_be_available_and_switch_to_it(
                    (By.XPATH, '//iframe[@title="Disqus"]')
                )
            )
            response_elements = self.wait.until(
                expected_conditions.presence_of_all_elements_located(
                    (By.XPATH, "//li[@class='post']")
                )
            )

            # for response in array of response elements
            for index, response in enumerate(response_elements):

                self.driver.implicitly_wait(2)

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

            self.driver.switch_to.default_content()

            # return temporary response container
            return temp_resp_container

        responses = get_responses()

        # return structured post data dictionary
        post_data.update({"responses": responses})
        return post_data

    def _find_posts(self) -> dict[dict, str]:
        def get_url_pairs(post) -> tuple:

            # get FCC post link attribute
            fcc_url = self._post_url_sanitizer(
                post.find_element(By.XPATH, ".//h2/a").get_attribute("href")
            )

            # get Disqus link attribute
            disqus_url = post.find_element(By.XPATH, ".//footer//a").get_attribute(
                "href"
            )

            return (fcc_url, disqus_url)

        def grab_text_from_new_tab(url: str, **xpaths) -> dict:
            """Opens a new tab, then goes to the specified URL
            within the new tab and grabs the element with the
            provided XPATH and function.

            Parameters
            ----------
            url : str
                the URL that the new tab should go to once opened

            xpath : str
                the XPATH of the element you wish to capture in the new tab
            """

            tmp_dict = {}

            # save main window
            main_window = self.driver.current_window_handle

            # open new blank tab
            self.driver.execute_script("window.open();")

            # switch to new window (second in window_handles array)
            self.driver.switch_to.window(self.driver.window_handles[1])

            # go to the new url in the new tab
            self.driver.get(url)

            for key, xpath in xpaths.items():

                # grab the wanted element and data
                tmp_dict[key] = self.driver.find_element(By.XPATH, xpath).text.replace(
                    "\n", " "
                )

                if "date" in key:
                    date = parser.parse(tmp_dict[key])
                    tmp_dict[key] = date.strftime("%Y-%m-%d %H:%M:%S")
                    tmp_dict.update({"date_epoch": date.timestamp()})

            # close this tab
            self.driver.close()

            # get back to the main window
            self.driver.switch_to.window(main_window)

            return tmp_dict

        # temp list to store each (Post_metadata, Disqus_link) grouping
        link_tuple_list: list[tuple] = []

        # use next-page method to load all posts
        print("[INFO] Identifying Posts...")
        self._next_page()

        # collect all loaded posts
        post_elements = wait.WebDriverWait(self.driver, 3).until(
            expected_conditions.presence_of_all_elements_located(
                (By.XPATH, "//div[@class='cards']/div")
            )
        )

        # for post in posts
        for post in post_elements:

            # generate url pairs (FCC, Disqus)
            fcc_url, disqus_url = get_url_pairs(post)

            # get post date element from FCC website
            post_metadata = grab_text_from_new_tab(
                fcc_url,
                title="//h1[@class='page__title title']",
                author="//div[@class='field field-name-field-author-fcc-leadership field-type-entityreference field-label-hidden author-block']/a",
                date="//span[@class='date-display-single']",
                content="(//div[@class='field-item even'])[2]",
            )

            # if date within date range (Now -> X)
            if parser.parse(post_metadata["date"]) >= self.age_threshold:

                # append to temp list
                link_tuple_list.append((post_metadata, disqus_url))

            # else break
            else:
                break

        # return temp list of urls
        return link_tuple_list

    def _new_post(self, index: int, post_metadata: dict) -> None:
        new_dict = {"post_id": index}
        new_dict.update(self._collect_page_metadata(index, post_metadata))
        self.posts.append(new_dict)

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
            url = url.replace(str_to_remove, "")

        return url

    def scrape(self):
        """Master function that will be called by user"""

        # wait a bit before starting scraping (implicit wait)
        self.driver.implicitly_wait(1)

        # go to base url
        self.goto(self.base_url)

        # find post urls for all pages (until posts are outside of date range)
        post_urls = self._find_posts()

        # if url's are found (there should be)
        if any(post_urls):

            # for each url identified
            for index, (post_metadata, disqus_url) in enumerate(post_urls):

                # tell the user the progress of scraping
                print("[INFO] Scraping post {}/{}...".format(index + 1, len(post_urls)))

                # go to post url
                self.goto(disqus_url)

                # Identify wanted page metadata and create new post structure
                self._new_post(index, post_metadata=post_metadata)

        # else
        else:
            # tell the user that no posts were found
            print("[WARNING] No posts found...")

        # convert generated dictionary structure to pandas DataFrame
        self.posts = pd.DataFrame(self.posts)

        # close the WebDriver Connection
        self.close()


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


if __name__ == "__main__":
    main()
