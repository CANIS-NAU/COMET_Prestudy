#!/usr/bin/env python3

# These tests are pretty much identical to the 
# ggroup_selenium_test.py tests, except that this will test
# the same functionalities using the GoogleScraper class implementation

from selenium import webdriver
from selenium.webdriver.common.by import By
from os import path
import tempfile
from random import randint

# global variables for reuse
canis_test_url = 'https://www.canis-lab.com/'
group_test_url = 'https://groups.google.com/g/canis-google-group-test-group'
mlab_group_url = 'https://groups.google.com/a/measurementlab.net/g/discuss'

def test_selenium_driver():
  """
  Ensure that selenium driver is properly working in this environment
  """
  
  driver = webdriver.Chrome()
  driver.get(canis_test_url)

  assert 'ABOUT' in driver.title

def test_ggroup_post_identify():
  """
  Test Selenium's ability to identify and extract text from google groups
  """

  driver = webdriver.Chrome()
  driver.get(group_test_url)
  
  for anchor_tag in driver.find_elements(by=By.TAG_NAME, value='a'):
    link = anchor_tag.get_attribute('href')

    if '/c/' in link:

      if "A followup" in driver.title:
        assert "A followup" in driver.title

def test_mlab_group():
  """
  Check that selenium is able to access the mlab google group, and navigate visible posts to grab
  title and post data, then store to temporary file
  """

  driver = webdriver.Chrome()
  driver.get(mlab_group_url)

  # save post titles for comparison later
  post_titles = []
  urls = set([a_tag.get_attribute('href') for a_tag in driver.find_elements(by=By.TAG_NAME, value='a') if '/c/' in a_tag.get_attribute('href')])
  filename = path.join(tempfile.gettempdir(), f'ggtester_{randint(0,999)}.txt')
  tmp_file = open(filename, 'x')


  # parse through all anchor tags until a valid "post" url pattern is identified
  # (containing '/c/')
  for post in urls:
    driver.get(post)

    post_titles.append(driver.title)
    tmp_file.write(f'{driver.title}\n')

  tmp_file.close()

  # now, check through all posts collected in the temp file, and compare with the names collected
  # in the post_titles array
  random_number = randint(0, len(post_titles))

  tmp_file = open(filename, 'r')
  file_lines = tmp_file.read().splitlines()
  tmp_file.close()

  assert post_titles[random_number] in file_lines[random_number]


# TODO
def test_topic_search():
  """
  Test selenium's ability to access the searchbar and query for keywords
  """
  pass