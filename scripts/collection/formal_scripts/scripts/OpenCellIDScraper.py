# imports
from dataclasses import dataclass
from BaseScraper import Scraper, DriverType, Post
from selenium.webdriver.common.by import By

# Post definitions
@dataclass
class OCellIDPost(Post):

    # TODO
    def to_str(self):
        """Convert data stored within the Post object into a string.
        This string will be used for data output to file later.
        """
        raise NotImplementedError


# Scraper definitions
class OCellIDScraper(Scraper):
    """Scraper object that specifically handles the OpenCellID forums (community.opencellid.org/)

    This object will function with the assumption that all scrape operations will
    occur **After** a query is sent to the website first. Because posts are loaded and removed
    based on the window's scroll location, until a stable solution is found, the main OpenCellID
    forums cant be parsed from the website's ``root`` directory. There **has** to be a 
    query sent through the site's search method first.
    """

    def __init__(self, base_url: str, keywords_file: str, driver: DriverType):
        super().__init__(base_url, keywords_file, driver)

    # TODO
    def _collect_page_metadata(self) -> dict:
        """When the desired page (a post containing all wanted data) is loaded,
        Identify the fields that need to be populated (within this object) and
        extract the data by whatever means necessary. Place the values into a dictionary
        that follows the format: { "field-name": "extracted-value", ... }

        Helper functions can be declared inside this method in order to keep things
        organized, but its no biggie.
        """

        def get_title():
            title_entity = self.driver.find_element(
                By.XPATH, "//a[@class='fancy-title']"
            )
            return title_entity.text

        # TODO
        def get_responses():
            pass

        # TODO
        def get_post_content():

            post_content_element = self.driver.find_element(By.XPATH, "")

            pass

        raise NotImplementedError

    def _find_posts(self) -> list[str]:
        """From the website root, identify all post items (defined below)
        that exist on the webpage. Return a list of URLs that correspond
        to each post item

        Returns
        -------
        list[str]
            A list of URLs for each identified post
        """

        # TODO - Determine if this is necessary after keyword search - use _next_page so that all posts are visible (scroll all the way down)
        # self._next_page()

        # if posts exist for this query
        posts_exist = (
            self.driver.find_element(By.XPATH, "//h3").text != "No results found."
        )
        if posts_exist:
            # grab all of the post url's
            all_post_urls = [
                post.get_attribute("href")
                for post in self.driver.find_elements(
                    By.XPATH, "//div[@class='fps-topic']/div[@class='topic']/a"
                )
            ]
            return all_post_urls

        else:
            return None

    # TODO
    def _new_post(self, keyword: str):
        """With the help of the _collect_page_metadata function,
        gather the post data, then place the data into the appropriate
        fields within a respective Post subclass

        Parameters
        ----------
        keyword : str
            The search term that was used to obtain this post as a result
        """
        raise NotImplementedError

    # TODO
    def _next_page(self):
        """In the case of OpenCellID, this page extends via scrolling down to
        the end of the page. Once at the bottom, the page will load more posts
        (~50) until the bottom of the page is reached again.

        This method will continuously scroll down to the bottom of the page
        until no more posts will be loaded. It will be assumed that there are
        no more posts that need to be loaded, and the process will continue towards
        scraping post urls from the fully loaded page.
        """

        raise NotImplementedError

    def search(self, search_term: str):
        """Takes a keyword, then generates a string that matches this website's
        method for creating "GET request' URLs. This string is then sent to the
        driver and emulate the keyword search. This method will result in the WebDriver
        being sent to the resulting query URL.

        Luckily, this happens to be the same method used for the Google Group scraper,
        muy nice :)

        Parameters
        ----------
        search_term : str
            The keyword/search-term you wish to query the website for
        """
        # format string to make manual get request
        get_syntax = "search?q="
        get_space_char = "%20"
        query = get_syntax + search_term.replace(" ", get_space_char)

        # go to the page with newly formatted request string for url
        self.goto(self.base_url + "/" + query)
