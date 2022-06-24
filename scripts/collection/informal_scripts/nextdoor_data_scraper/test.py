from lib2to3.pgen2 import driver
from logging import exception
from pydoc import classname
from debugpy import configure
from jmespath import search
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, requests, random, pandas as pd, datetime, calendar, re
from datetime import datetime as dt
from dateutil.relativedelta import *
from os.path import exists

def configure_driver(chromedriver: str):
    """Configure the chromedriver

    Parameters
    ----------
    chromedriver : str
        File path of the chromedriver in string form

    Returns
    ----------
    webdriver
        The configured webdriver
    """

    # configure webdriver
    options = Options()
    options.page_load_strategy = 'normal'
    options.add_argument('--disable-site-isolation-trials')

    # return webdriver
    return webdriver.Chrome(options=options, executable_path=chromedriver)

def login(username: str, password: str):
    """Log in to Nextdoor

    Parameters
    ----------
    username : str
        Username that will be used for the email/phone number input

    password : str
        Password that will be used for the password option
    """

    # go to the nextdoor webpage
    driver.get('https://nextdoor.com/login/?ucl=1')
    time.sleep(5)

    # input username
    username_input = driver.find_element(By.CSS_SELECTOR, 'input.css-bs4yd9')
    username_input.send_keys(username)

    # input password
    password_input = driver.find_element(By.CSS_SELECTOR, 'input.css-62beto.password_text_input')
    password_input.send_keys(password)

    # click login button
    login_button = driver.find_element(By.CSS_SELECTOR, 'button.css-1hpv9ll')
    driver.execute_script("arguments[0].click();", login_button)
    time.sleep(random.randint(2, 5))

def scroll_page():
    """Scroll through the results page until all posts are available
    """

    # get the height of the web page
    last_height = driver.execute_script('return document.body.scrollHeight')

    # scroll while the end of the page hasn't been reached
    while True:
        break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(5)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height

def main():

    dates = []

    global driver

    driver = configure_driver(r"C:\Users\kylie\Documents\chromedriver.exe")

    login('knc334@nau.edu', 'yoMama132')

    driver.get('https://nextdoor.com/search/posts/?ccid=7E25E89B-7923-4364-A11B-20E127E181E1&navigationScreen=FEED&ssid=BC6802A2-6432-4887-884E-789810B2F4E2&query=' + 'internet')

    time.sleep(5)

    scroll_page()

    post_tops = driver.find_elements(By.CSS_SELECTOR, 'div.css-1msysi4')

    for post_top in post_tops:

        neighborhood_date_elements = post_top.find_elements(By.CSS_SELECTOR, 'div.css-1l73x44')

        if len(neighborhood_date_elements) > 0:

            neighborhood_date_element = neighborhood_date_elements[0]

            date = neighborhood_date_element.text.split('·')[1]

            date = date.strip()
            date = re.split('(\d+)', date)
            print(date)
            date = ''.join(date[2:])
            date.strip()

            if date not in dates:

                dates.append(date)
                print(date)

    print(dates)

if __name__ == '__main__':
    main()