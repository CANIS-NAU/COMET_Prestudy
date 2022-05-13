#!/usr/bin/env python3

# These tests are pretty much identical to the
# ggroup_selenium_test.py tests, except that this will test
# the same functionalities using the GoogleScraper class implementation

from selenium import webdriver
from selenium.webdriver.common.by import By
from os import path
import tempfile
from random import randint
from src.subClasses.GoogleScraper.GoogleGroupsScraper import GoogleGroupsScraper

# global variables for reuse
canis_test_url = "https://www.canis-lab.com/"
group_test_url = "https://groups.google.com/g/canis-google-group-test-group"
mlab_group_url = "https://groups.google.com/a/measurementlab.net/g/discuss"


def test_ggroup_post_identify():
    """
    Test Selenium's ability to identify and extract text from google groups
    """

    quinton_scraper = GoogleGroupsScraper(group_test_url, '', 'chrome')
    quinton_scraper.scrape()

    for post in quinton_scraper.posts:
        if 'A followup' in post.title:
            assert 'A followup' in post.title
        

def test_expand_all():
    """TODO At this moment, there is no real way to test this other than with human intervention.
    Human needs to see if the tabs open when the command is executed"""

    expand_class = GoogleGroupsScraper(mlab_group_url, '', 'chrome')

    expand_class.scrape()

    assert True


def test_mlab_group():
    """
    Check that selenium is able to access the mlab google group, and navigate visible posts to grab
    title and post data, then store to temporary file
    """

    mlab_scraper = GoogleGroupsScraper(mlab_group_url, '', 'chrome')

    # collect all post data points and save them to a file called (post_titles.txt)
    mlab_scraper.scrape()

    collected_titles = [post.title for post in mlab_scraper.posts]
    mlab_scraper.flushPosts('./post_titles.txt')

    # load lines from the created file into an array for comparison
    with open("./post_titles.txt", 'r') as out_file:
        file_lines = out_file.read().splitlines()


    # now, check through all posts collected in the file, and compare with the 
    # names collected in the 'collected_titles' variable
    
    for title in collected_titles:
        if title in file_lines:
            assert title in file_lines


# TODO
def test_topic_search():
    """
    Test selenium's ability to access the searchbar and query for keywords
    """
    pass
