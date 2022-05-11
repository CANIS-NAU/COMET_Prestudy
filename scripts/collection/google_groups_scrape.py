#!/usr/bin/env python3

# imports
from selenium import webdriver

# global variables (keep minimal)
    # google group url to parse


# Initialize selenium
def _init_selenium(chrome_flag: bool):
    if chrome_flag:
        return webdriver.Chrome()
    else:
        return webdriver.Firefox()



# navigate to the google groups website in question

# identify valid posts
    # extract title information

    # extract post body

    # recursively extract each reply from each post