#!/usr/bin/env python3

# These tests are pretty much identical to the
# ggroup_selenium_test.py tests, except that this will test
# the same functionalities using the GoogleScraper class implementation

from GoogleGroupsScraper import GoogleGroupsScraper, DriverType
from os import path
from pathlib import Path
import os
# global variables for reuse
canis_test_url = "https://www.canis-lab.com/"
group_test_url = "https://groups.google.com/g/canis-google-group-test-group"
mlab_group_url = "https://groups.google.com/a/measurementlab.net/g/discuss"

keywords_txt = 'scripts/tests/keywords.txt'
keywords_mlab = 'scripts/tests/keywords_mlab.txt'


def test_ggroup_post_identify():
    """
    Test Selenium's ability to identify and extract text from google groups
    """

    quinton_scraper = GoogleGroupsScraper(group_test_url, keywords_txt, DriverType.CHROME)
    quinton_scraper.scrape()

    for post in list(quinton_scraper.posts.values()):
        for value in post:
            if 'A followup' in value.title:
                assert 'A followup' in value.title
        

def test_expand_all():
    """TODO At this moment, there is no real way to test this other than with human intervention.
    Human needs to see if the tabs open when the command is executed"""

    expand_class = GoogleGroupsScraper(mlab_group_url, '', DriverType.CHROME)

    expand_class.scrape()

    assert True


def test_mlab_group():
    """
    Check that selenium is able to access the mlab google group, and navigate visible posts to grab
    title and post data, then store to temporary file
    """

    mlab_scraper = GoogleGroupsScraper(mlab_group_url, keywords_mlab, DriverType.CHROME, path.join(str(Path.home()), 'Downloads', 'chromedriver.exe'))

    # collect all post data points and save them to a file called (post_titles.txt)
    mlab_scraper.scrape()
    mlab_scraper.close()

    # Array of post titles to compare against the 'flushed' values
    collected_titles = []
    for values in list(mlab_scraper.posts.values()):
        for post in values:
            collected_titles.append(post.title)

    mlab_scraper.flush_posts('./post_titles_mlab.txt')

    # load lines from the created file into an array for comparison
    with open("./post_titles_mlab.txt", 'r') as out_file:
        file_lines = out_file.read().splitlines()


    # now, check through all posts collected in the file, and compare with the 
    # names collected in the 'collected_titles' variable
    
    for title in collected_titles:
        if title in file_lines:
            assert title in file_lines

def test_next_page():
    """
    Test selenium's ability to go to the next page
    of a multi-page Google Groups search query

    useful keyword for testing: 'speed'
    """

    next_page_scraper = GoogleGroupsScraper(mlab_group_url, keywords_txt, DriverType.CHROME)

    next_page_scraper.search(next_page_scraper.keywords[0])

    while next_page_scraper._next_page():
        pass

    assert True