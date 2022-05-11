#!/usr/bin/env python3

# imports 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from abc import abstractclassmethod, ABC

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
    self.driver = self._get_driver()

  @abstractclassmethod
  def search(self, search_term: str):
    """Enter keyword search into the desired page. Returns the selenium driver object with the loaded-page results

    Args:
        search_term (str): search term that will be queried by the website

    Returns:
        WebDriver: selenium WebDriver object with the post-query search results page
    """
    pass

  @abstractclassmethod
  def next_page(self):
    pass

  @abstractclassmethod
  def scrape(self):
    pass

  @abstractclassmethod
  def parse_replies(self):
    pass


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