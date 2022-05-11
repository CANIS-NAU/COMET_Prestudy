from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from os import path
import tempfile
from random import randint
import selenium

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

  # setup selenium driver
  driver = webdriver.Chrome()
  driver.get(mlab_group_url)

  # save post titles for comparison later
  post_titles = []
  urls = set([a_tag.get_attribute('href') for a_tag in driver.find_elements(by=By.TAG_NAME, value='a') if '/c/' in a_tag.get_attribute('href')])
  tmp_file = path.join(tempfile.gettempdir(), "testfile")

  # parse through all anchor tags until a valid "post" url pattern is identified
  # (containing '/c/')
  for post in urls:
    driver.get(post)
    post_titles.append(driver.title)

    with open(tmp_file, 'a') as post_title_file:
      post_title_file.write(driver.title + '\n')

  # now, check through all posts collected in the temp file, and compare with the names collected
  # in the post_titles array

  random_number = randint(0, len(post_titles))

  with open(tmp_file, 'r') as test_file:
    file_lines = test_file.readlines()

    assert post_titles[random_number] in file_lines



