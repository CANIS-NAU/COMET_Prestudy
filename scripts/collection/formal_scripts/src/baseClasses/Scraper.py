#!/usr/bin/env python3

# imports
from selenium import webdriver
from abc import abstractmethod, ABC
from .Post import Post

# Class definition
class Scraper(ABC):

    ######## Public Methods ########
    def __init__(self, base_url: str, search_keywords: list, driver: str):
        """Initialize the Scraper Object

        NOTE: Web drivers need to be installed prior to use

        Args:
            base_url (str): The url of the root website you wish to scrape
            search_keywords (list): Specific keywords/search terms that you wish to enter into a search functionality
            driver (str): The driver/browser you wish to use for accessing the internet ("Chrome"/"Firefox/Safari/Opera")
        """

        self.base_url: str = base_url
        self.search_keywords: list[str] = search_keywords
        self.driver = self._get_driver(driver)
        self.posts: list[Post] = []

    ######## Needs Implementation ########

    @abstractmethod
    def search(self, search_term: str):
        """Enter keyword search into the desired page. Returns the selenium driver object with the loaded-page results

        Args:
            search_term (str): search term that will be queried by the website

        Returns:
            WebDriver: selenium WebDriver object with the post-query search results page
        """
        pass

    @abstractmethod
    def next_page(self):
        """Technique for moving to the next page of a pagenated website, or loading all data points
        from a dynamically growing page structure.
        """
        pass

    @abstractmethod
    def get_post_metadata(self):
        """meta-function, grabs current post metadata. (ie. Post title, post text contents, responses, attached media, etc.)

        Returns:
            Post: Post data object with post elements stored as class members
        """

    @abstractmethod
    def get_post_title(self):
        """Get the title of a post/place of interest"""
        pass

    @abstractmethod
    def get_post_responses(self):
        """Get all responses from the specified post url

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """

    @abstractmethod
    def get_post_text_content(self):
        """get the direct text content from within the post (ie. post author's text)"""

    @abstractmethod
    def scrape(self):
        """meta-function for conducting all scrape operations.
        Acts as an entrypoint for all functionality
        """
        pass

    @abstractmethod
    def to_post(self):
        """Convert the currently loaded page to a post object, then save within
        the scraper's collection
        """
        pass

    ########## END - Needs Implementation ##########

    def goto(self, url):
        """Navigate to the page specified by the `url` parameter

        Args:
            url (str): the url of the website you wish to navigate to with selenium
        """

        self.driver.get(url)

    def to_baseurl(self):
        """Take the browser back to the website root"""

        self.driver = self.driver.get(self.base_url)

    ######## Private Class Functions ########
    def _get_driver(self, driver_name: str):
        """Based on input, return a driver object that
        corresponds to the required web browser

        Args:
            driver_name (str): name of the driver that is desired; Options: "Chrome, Firefox, Opera, Safari"

        Returns:
            WebDriver: The driver object of the requested web browser
        """
        if "chrome" in driver_name.lower():
            return webdriver.Chrome()

        elif "firefox" in driver_name.lower():
            return webdriver.Firefox()

        elif "safari" in driver_name.lower():
            return webdriver.Safari()

        elif "opera" in driver_name.lower():
            return webdriver.Opera()

        else:
            raise Exception("Invalid driver name")
