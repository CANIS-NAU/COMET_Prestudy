#!/usr/bin/env python3

# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import Scraper

# global variables (keep minimal)
    # google group url to parse


# Initialize selenium
class GoogleGroupsScraper(Scraper):

    def __init__(self, site_url: str, keywords: list):
        super().__init__()

    def _init_selenium(chrome_flag: bool):
        """Create a selenium Driver object, based on flag value

        Args:
            chrome_flag (bool): If true, will use Google Chrome driver (chromedriver), else will use Firefox (geckodriver)

        Returns:
            _type_: The web driver object to be further manipulated
        """
        
            return webdriver.Chrome()
        else:
            return webdriver.Firefox()



# navigate to the google groups website in question

# identify valid posts
    # extract title information

    # extract post body

    # recursively extract each reply from each post