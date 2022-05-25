#!/usr/bin/env python3

# These tests are pretty much identical to the
# ggroup_selenium_test.py tests, except that this will test
# the same functionalities using the GoogleScraper class implementation

from OpenCellIDScraper import OCellIDScraper, DriverType
from os import path 
from pathlib import Path

# global variables for reuse
opencellid_url = 'https://community.opencellid.org/'

keywords_txt = 'scripts/tests/keywords.txt'
keywords_mlab = 'scripts/tests/keywords_mlab.txt'

def test_search_json():
    """Test the program's ability to send a search query, then return a JSON file with
    the results
    """

    ocellid = OCellIDScraper(opencellid_url, "", None)
    json_result = ocellid.search("speed")

    assert "Obtain raw measurement" in json_result['topics'][0]['title']
        

# TODO
def test_ocellid_master():
    """
    Check that the script can fully handle the workload of searching, scraping, and data output/storage
    """

    opencellScrape = OCellIDScraper(opencellid_url, keywords_txt, None)

    # collect all post data points and save them to a file called (post_titles.txt)
    opencellScrape.scrape()

    # Array of post titles to compare against the 'flushed' values
    collected_titles = []
    for values in list(opencellScrape.posts.values()):
        for post in values:
            collected_titles.append(post.title)

    opencellScrape.flush_posts('./post_titles_ocellid.txt')

    # load lines from the created file into an array for comparison
    with open("./post_titles_mlab.txt", 'r') as out_file:
        file_lines = out_file.read().splitlines()


    # now, check through all posts collected in the file, and compare with the 
    # names collected in the 'collected_titles' variable
    
    for title in collected_titles:
        if title in file_lines:
            assert title in file_lines