#!/usr/bin/env python3

# imports
from selenium import webdriver
from abc import abstractmethod, ABC

# Class definition
class Scraper(ABC):

    ######## Public Methods ########
    def __init__(self, site_url: str, keywords: list, driver: str):
        """Initialize the Scraper Object

        Args:
            site_url (str): The url of the website you wish to scrape
            keywords (list): Specific keywords/search terms that you wish to enter into a search functionality
            driver (str): The driver/browser you wish to use for accessing the internet ("Chrome"/"Firefox")
        """

        self.site_url = site_url
        self.keywords = keywords
        self.driver = self._get_driver(driver)
        self.posts = []

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
    def get_post_metadata():
        """meta-function, grabs current post metadata. (ie. Post title, post text contents, responses, attached media, etc.)

        Returns:
            Post: Post data object with post elements stored as class members
        """

    @abstractmethod
    def get_post_title():
      """Get the title of a post
      """
      pass

    @abstractmethod
    def get_post_text_content():
      """get the direct text content from within the post (ie. post author's text)
      """

    @abstractmethod
    def scrape(self):
        """meta-function for conducting all scrape operations.
        Acts as an entrypoint for all functionality
        """
        pass

    def goto(self, url):
        """Navigate to the page specified by the `url` parameter

        Args:
            url (str): the url of the website you wish to navigate to with selenium
        """

        self.driver = self.driver.get(url)

    ######## Private Class Functions ########
    def _get_driver(driver_name: str):
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
