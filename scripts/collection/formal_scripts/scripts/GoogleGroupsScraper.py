#!/usr/bin/env python3

# imports
import argparse
from time import sleep
from BaseScraper import Scraper
from selenium.webdriver.common.by import By
import pandas as pd
import hashlib


class GoogleGroupsScraper(Scraper):

    ########## Public Methods ##########
    def __init__(self, site_url: str, keywords_file: str, driver: str):
        super().__init__(site_url, keywords_file, driver)

    def _next_page(self, keyword) -> bool:
        """For Google Groups, this function handles moving to the
        next page to gather more data from subsequent 'paginated' pages

        Returns
        -------
        bool
            If True, there are still pages that need to be grabbed, continue
            the operation. If False, we have reached the end of the pages, stop
            the operation.
        """

        #identify 'next page' button
        next_page_button = self.driver.find_element(By.XPATH, "(//div[@role='button' and @aria-label='Next page'])[last()]")
        sleep(1)
        #next_page_button = self.driver.find_elements(By.XPATH,"(//div[@role='button' and @aria-label='Next page'])")[-1]

        

        #next_page_button_parent = self.driver.find_element(By.XPATH, "")

        # if next page button is available
        tab_index = int(next_page_button.get_attribute('tabindex'))
        is_visible =  tab_index == 0
        if is_visible:
            # click the button
            next_page_button.click()
            return True

        # else
        else:
            # let the user know that this is the last page of the website
            print("[INFO] Last page reached for Keyword: {}".format(keyword))
            return False

    def scrape(self):

        # iterate through all provided keywords
        for keyword in self.keywords:

            # search
            print("[INFO] Searching With Keyword: {}".format(keyword))
            self.search(keyword)

            # collect post urls from search query
            post_urls = self._find_posts(keyword)

            # if results exist
            if post_urls:

                print("[INFO] {} results found for keyword: {}".format(len(post_urls), keyword))

                # store item into the Scraper.posts dictionary
                for iter, post in enumerate(post_urls):
                    print("[INFO] Scraping Post {}/{}".format(iter+1, len(post_urls)))
                    self.goto(post)
                    self._new_post()

            # else
            else:
                # tell the user that there were no results for this keyword
                print(f"[INFO] No results for keyword: {keyword}")

        self.posts = pd.DataFrame(self.posts).drop_duplicates(subset=['post_id'])
        print("[INFO] Removing Duplicates")
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
    def _find_posts(self, keyword) -> list[str]:
        """Identify new posts on current page.

        In the case of Google Groups, all posts are all filtered <a> tags
        containing '/c/' located in the root page

        Returns:
            list[str]: list of urls for all identified posts located in the group
        """

        parsed_links = []

        # emulation of a do-while loop
        while True:

            # grabs all of the clickable links to each post (no duplicates) and returns array of links
            if any(self.driver.find_elements(By.XPATH, "//div[@role='main']/h1")):
                return None

            else:
                post_links = self.driver.find_elements(
                    By.XPATH, "//div[@role='gridcell']/a[contains(@href, '/c/')]"
                )
                for links in post_links:
                    parsed_links.append(links.get_attribute("href"))

            if not self._next_page(keyword):
                break

        return parsed_links

    def _collect_page_metadata(self) -> dict:
        """When the desired page (a post containing all wanted data) is loaded,
        Identify the fields that need to be populated (within this object) and
        extract the data by whatever means necessary. Place the values into a dictionary
        that follows the format: { "field-name": "extracted-value", ... }
        """
        self._expand_all_posts()

        title = self.driver.title.lower().replace(' ', '-')
        author = self._get_post_author()
        content = self._get_content()
        replies = self._get_responses()
        
        post_id = int(hashlib.md5(title.encode()).hexdigest(), 16)
        return {
            "post_id": post_id,
            "title": title,
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
            expand_button.pop().click()

    def _new_post(self):
        """After collecting all post data, use this function to
        organize and place the data in their appropriate fields
        within the class.
        """
        metadata = self._collect_page_metadata()
        self.posts.append(metadata)
        

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
        value = self.driver.find_element(By.XPATH, "(//div[@role='region' ])[1]").text
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
        # find lists of authors and their replies
        author_str = self.driver.find_elements(By.XPATH, "(//h3)[position()>1]")
        response_str = self.driver.find_elements(
            By.XPATH, "(//div[@role='region' ])[position()>1]"
        )

        # stitch together both lists into dictionary with structure {author:response}
        value = {
            author_str[iter].text: response_str[iter].text
            for iter in range(len(response_str))
        }
        return value


# lastly, we implement a main method to make this script executable 
def main():
    default_group_url = "https://groups.google.com/a/measurementlab.net/g/discuss"

    parser = argparse.ArgumentParser(description="Script for scraping MLab google groups discussion forum")
    parser.add_argument('keywords_dir', help='path to the file where all keywords are listed', type=str)
    parser.add_argument('data_out', type=str, help="path+filename of the outputted tsv/csv file")
    parser.add_argument('--driver', '-d', type=str, help="The browser you plan to use for scraping. Defaults to Google Chrome.", default='chrome', choices=['chrome', 'firefox', 'opera', 'safari'])


    args = parser.parse_args()

    google_groups_scraper = GoogleGroupsScraper(default_group_url, args.keywords_dir, args.driver)
    google_groups_scraper.scrape()

    google_groups_scraper.flush_posts(args.data_out)

if __name__ == '__main__':
    main()