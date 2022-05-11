#!/usr/bin/env python3

# imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from baseClasses.Scraper import Scraper

# global variables (keep minimal)
    # google group url to parse


# Initialize selenium
class GoogleGroupsScraper(Scraper):

    def __init__(self, site_url: str, keywords: list, driver: str):
        super().__init__()



# navigate to the google groups website in question

# identify valid posts
    # extract title information

    # extract post body

    # recursively extract each reply from each post