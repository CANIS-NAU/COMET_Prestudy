from logging import exception
from pydoc import classname
from debugpy import configure
from jmespath import search
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import random
import pandas as pd
import datetime
import calendar
import re
import pickle
import os
from datetime import datetime as dt
from dateutil.relativedelta import *
from os.path import exists

start_year = None
MONTHS = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
          'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

driver = None

def configure_driver():
    global driver

    # configure webdriver
    options = Options()
    options.add_argument('--disable-notifications')
    options.page_load_strategy = 'normal'
    options.add_argument('--disable-site-isolation-trials')

    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    options = Options()
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))


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
    password_input = driver.find_element(
        By.CSS_SELECTOR, 'input.css-62beto.password_text_input')
    password_input.send_keys(password)

    # click login button
    login_button = driver.find_element(By.CSS_SELECTOR, 'button.css-1hpv9ll')
    driver.execute_script("arguments[0].click();", login_button)
    time.sleep(random.randint(2, 5))


def create_output_file(output_file: str):
    """Create the tsv file that will be used to store data

    Parameters
    ----------
    output_file : str
        The tsv file name and file path that holds all of the scraped data from Nextdoor
    """

    # create pandas dataframe as a tsv file and create the file in the specified location given
    dataframe = pd.DataFrame(columns=['author', 'neighborhood', 'date', 'text', 'category',
                             'media list', 'num comments', 'num reactions', 'reactions'])
    dataframe.to_csv(output_file, sep='\t')


def create_keyword_string(keywords_file: str):
    """Create the string that will be used to search for the keywords

    Parameters
    ----------
    keywords_file : str
        The txt file path that stores the keywords to search for in string form

    Returns
    ----------
    keyword_string : str
        A string of keywords to search for 
    """

    # declare variables
    keyword_string = ''

    # open the keywords file and list each keyword
    keywords_file = open(keywords_file, 'r')
    keywords = list(keywords_file)

    # add the keywords to a string for searching
    for keyword in keywords:
        keyword = keyword.replace('\n', '')
        keyword_string += keyword + '%20'

    # return the keyword string
    return keyword_string


def scroll_page():
    """Scroll through the results page until all posts are available
    """

    # get the height of the web page
    last_height = driver.execute_script('return document.body.scrollHeight')

    # scroll while the end of the page hasn't been reached
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(5)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height


def get_post_media(post: object):
    """Gather the media of the given post

    Parameters
    ----------
    post : WebElement
        The post WebElement to look into

    Returns
    ----------
    media_list : list
        A list of media urls that are in the post
    """

    # get the post media containers
    media_containers = post.find_elements(By.CSS_SELECTOR, 'img._33jGwce4')
    media_list = []

    # loop through each container and get the source or url
    for media_container in media_containers:
        media_list.append(media_container.get_attribute('src'))

    # return the media list
    return media_list


def scroll_reactions():
    reaction_page = driver.find_elements(By.CSS_SELECTOR, 'div.css-zulrf6')

    if len(reaction_page) > 0:
        last_height = driver.execute_script(
            'return arguments[0].scrollHeight', reaction_page[0])
        while True:
            driver.execute_script(
                "arguments[0].scrollTo(0, arguments[0].scrollHeight)", reaction_page[0])
            time.sleep(5)
            new_height = driver.execute_script(
                'return arguments[0].scrollHeight', reaction_page[0])
            if new_height == last_height:
                break
            last_height = new_height


def get_reactions(post: object, type: str):
    """Gather the reactions of the post

    Parameters
    ----------
    post : WebElement
        The post WebElement to look into

    type : str
        The type of post being looked at, ex: 'comment' or 'post'

    Returns
    ----------
    reactions : dict[str, list]
        A dictionary of the possible reactions with a list of users that made that reaction

    None
        Nothing if there were no reactions
    """

    # get the correct reactions button based on whether the WebElement is a post or comment
    if type == 'post':
        reactions_button = post.find_elements(
            By.CSS_SELECTOR, 'button._1p1i18kz.post-action-count-container-reaction-count.post-action-space-if-not-last-child._15-DWJ4U.button-text')
    elif type == 'comment':
        reactions_button = post.find_elements(
            By.CSS_SELECTOR, 'button._1p1i18kz._15-DWJ4U.button-text')

    # if a reactions button does exist
    # click on the button and gather each reaction and who did that reaction
    if len(reactions_button) > 0:
        driver.execute_script("arguments[0].click();", reactions_button[0])
        time.sleep(random.randint(2, 5))

        scroll_reactions()

        who_reacted = driver.find_elements(By.CSS_SELECTOR, 'h2.css-up964u')
        who_reacted = [name.text for name in who_reacted]

        reaction_divs = driver.find_elements(By.CSS_SELECTOR, 'div.css-clcwj9')
        reactions = {'Like': [], 'Thank': [],
                     'Agree': [], 'Haha': [], 'Wow': [], 'Sad': []}
        for reaction in reaction_divs:
            reaction_img = reaction.find_elements(By.CSS_SELECTOR, 'img')[
                1].get_attribute('alt')
            reaction_person = reaction.find_element(
                By.CSS_SELECTOR, 'h2.css-up964u').text

            if reaction_img == 'Like':
                reactions['Like'].append(reaction_person)
            if reaction_img == 'Thank':
                reactions['Thank'].append(reaction_person)
            if reaction_img == 'Agree':
                reactions['Agree'].append(reaction_person)
            if reaction_img == 'Haha':
                reactions['Haha'].append(reaction_person)
            if reaction_img == 'Wow':
                reactions['Wow'].append(reaction_person)
            if reaction_img == 'Sad':
                reactions['Sad'].append(reaction_person)

        # exit the reactions container
        exit_button = driver.find_element(
            By.CSS_SELECTOR, 'div.css-5qiylr').find_element(By.CSS_SELECTOR, 'div.css-dkr4zn')
        driver.execute_script("arguments[0].click();", exit_button)
        time.sleep(random.randint(2, 5))

        # return the reactions
        return reactions

    # otherwise, there are no reactions
    else:

        # return nothing, since there are no reactions
        return None


def upload_data(data: list, output_file: str):
    """Add the row of data to the given output file

    Parameters
    ----------
    data : list
        Dictionary of data

    output_file : str
        The output file given in the arguments
    """
    df = pd.DataFrame(data)
    df.to_csv(output_file, mode='a', sep='\t', header=False)


def get_comment_data():
    """Gathers the data of each comment of a post

    Parameters
    ----------
    output_file : str
        The output file given in the arguments
    """

    # get the comments of the post
    comments = driver.find_elements(By.CSS_SELECTOR, 'div.js-media-comment')

    data = []

    # loop through each comment and gather its data
    for comment in comments:

        data.append({
            'author': comment.find_elements(By.CSS_SELECTOR, 'a.comment-detail-author-name')[0].text if len(comment.find_elements(By.CSS_SELECTOR, 'a.comment-detail-author-name')) > 0 else None,
            'neighborhood': comment.find_elements(By.CSS_SELECTOR, 'a.PH4qbR1K')[0].text if len(comment.find_elements(By.CSS_SELECTOR, 'a.PH4qbR1K')) > 0 else None,
            'date': comment.find_elements(By.CSS_SELECTOR, 'span.css-ra9tcg')[0].text if len(comment.find_elements(By.CSS_SELECTOR, 'span.css-ra9tcg')) > 0 else None,
            'text': comment.find_elements(By.CSS_SELECTOR, 'span.Linkify')[0].text if len(comment.find_elements(By.CSS_SELECTOR, 'span.Linkify')) > 0 else None,
            'posted in': main_post.find_elements(By.CSS_SELECTOR, 'div.css-m9gd8r')[0].text if len(main_post.find_elements(By.CSS_SELECTOR, 'div.css-m9gd8r')) > 0 else None,
            'media list': get_post_media(comment) if get_post_media(comment) != [] else None,
            'comments': None,
            'reactions': get_reactions(comment, 'comment')
        })

    return data


def get_main_post_data(output_file):
    """Gathers the data of each comment of a post

    Parameters
    ----------
    output_file : str
        The output file given in the arguments
    """

    # get global main post element
    global main_post

    # get the main post
    main_post = driver.find_element(
        By.CSS_SELECTOR, 'div.js-media-post.clearfix.post')

    text = main_post.find_elements(By.CSS_SELECTOR, 'span.Linkify')[0].text if len(main_post.find_elements(By.CSS_SELECTOR, 'span.Linkify')) > 0 else None

    if text:

        for keyword in keyword_list:

            if keyword.lower() in text.lower():

                # gather the data of the main post
                data = [{
                    'author': main_post.find_elements(By.CSS_SELECTOR, 'a._1QrCPIoo._2nXsqARR')[0].text if len(main_post.find_elements(By.CSS_SELECTOR, 'a._1QrCPIoo._2nXsqARR')) > 0 else None,
                    'neighborhood': main_post.find_elements(By.CSS_SELECTOR, 'a.post-byline-redesign')[0].text if len(main_post.find_elements(By.CSS_SELECTOR, 'a.post-byline-redesign')) > 0 else None,
                    'date': main_post.find_elements(By.CSS_SELECTOR, 'a.post-byline-redesign')[1].text if len(main_post.find_elements(By.CSS_SELECTOR, 'a.post-byline-redesign')) > 0 else None,
                    'text': text,
                    'posted in': main_post.find_elements(By.CSS_SELECTOR, 'div.css-m9gd8r')[0].text if len(main_post.find_elements(By.CSS_SELECTOR, 'div.css-m9gd8r')) > 0 else None,
                    'media list': get_post_media(main_post) if get_post_media(main_post) != [] else None,
                    'comments': get_comment_data(),
                    'reactions': get_reactions(main_post, 'post')
                }]

                upload_data(data, output_file)

                break


def open_see_more_links():
    """Open all of the 'see more' links on the page
    """

    # find all of the see more buttons
    see_more_buttons = driver.find_elements(
        By.CSS_SELECTOR, 'button.see-previous-comments-button-paged._1eW-tOzA')

    # while see more buttons exist
    while len(see_more_buttons) > 0:

        # open them
        driver.execute_script("arguments[0].click();", see_more_buttons[0])
        time.sleep(random.randint(2, 5))

        # check for more
        see_more_buttons = driver.find_elements(
            By.CSS_SELECTOR, 'button.see-previous-comments-button-paged._1eW-tOzA')


def check_year(post: object, start_year: str):

    post_top = driver.find_elements(By.CSS_SELECTOR, 'div.css-1msysi4')

    if len(post_top) > 0:

        post_top = post_top[0]

        neighborhood_date_elements = post_top.find_elements(
            By.CSS_SELECTOR, 'div.css-1l73x44')

        if len(neighborhood_date_elements) > 0:

            neighborhood_date_element = neighborhood_date_elements[0]

            if '·' not in neighborhood_date_element.text:

                return False

            date = neighborhood_date_element.text.split('·')[1]
            date = date.strip()

            date = re.split('(\d+)', date)
            date = [element.strip() for element in date if element != '']

            if len(date) == 2:

                year = dt.today().year
                month = dt.today().month
                day = dt.today().day

                months_strings = list(MONTHS.keys())
                months_nums = list(MONTHS.values())

                date_day = date[0]
                date_month = date[1]

                if date_month in months_strings:
                    date_month_num = months_nums[months_strings.index(
                        date_month)]

                    if date_month_num > month:

                        post_year = year - 1

                        if int(post_year) >= int(start_year):

                            return True

                    else:

                        return True

            elif len(date) == 3:

                date_year = '20' + date[2]
                date = int(date_year)

                if int(date_year) >= int(start_year):

                    return True

    return False


def create_keyword_list(keywords_file):

    file = open(keywords_file, 'r')
    keywords = []

    for keyword in file:

        keyword = keyword.replace('\n', '')
        keywords.append(keyword)

    return keywords


def NextdoorScraper(limit, username, password, keywords_file, output_file):
    """Scrape Nextdoor using the given keywords and produce a tsv file with the data found

    Parameters
    ----------
    limit : int
        The number of posts to collect, as long as there are enough available

    username : str
        Username that will be used for the email/phone number input

    password : str
        Password that will be used for the password option

    keywords_file : str
        The file that holds all keywords to be searched in Nextdoor; Format: 'Internet/nWifi/nSpeed'

    output_file : str
        The tsv file name and file path that holds all of the scraped data from Nextdoor

    chromedriver : str
        The file path to the chromedriver
    """

    # declare global variables
    global driver, start_year, keyword_list

    if os.path.exists('oldposts.dat'):

        print('\n*****Old posts that did not have data gathered have been found.*****')
        print('\n*****Would you like to use them?*****')

        answer = input('Y (yes) or N (no): ')

        if answer.lower() == 'y':

            print('\n*****Proceeding per usual.*****')

        elif answer.lower() == 'n':

            os.remove('oldposts.dat')
            print('\n*****Proceeding per usual.*****')

        else:

            print('\n*****Your response was not applicable. Proceeding per usual.*****')

    # create the output file
    create_output_file(output_file)

    # create the keyword string
    keyword_string = create_keyword_string(keywords_file)
    keyword_list = create_keyword_list(keywords_file)

    configure_driver()

    # login to nextdoor
    login(username, password)

    # search for the given keyword posts
    driver.get('https://nextdoor.com/search/posts/?ccid=7E25E89B-7923-4364-A11B-20E127E181E1&navigationScreen=FEED&ssid=BC6802A2-6432-4887-884E-789810B2F4E2&query=' + keyword_string)
    time.sleep(5)

    if os.path.exists('oldposts.dat'):

        hrefs = pickle.load(open('oldposts.dat', 'rb'))

        print('\n*****There are', len(hrefs),
              'posts to collect data from.*****')

    else:

        # scroll through the entire page
        scroll_page()

        # get the posts shown
        posts = driver.find_elements(
            By.CSS_SELECTOR, 'a._2pCkWHax.css-1q9s7yp')

        for post in posts:

            if not check_year(post, start_year):

                posts.remove(post)

        # if there are no posts
        # let the user know and quit
        if len(posts) == 0:
            print('No posts were found with the arguments given.')
            quit()

        # if there is a limit
        # only get the limit number of posts
        if limit != None:
            if limit < len(posts):
                posts = posts[0:limit]

        hrefs = []

        # loop through each post and get their hrefs
        for post in posts:
            href = post.get_attribute('href')
            hrefs.append(href)

        print('\n*****There are', len(hrefs),
              'posts to collect data from.*****')

        pickle.dump(hrefs, open('oldposts.dat', 'wb'))


    # loop through each href
    for href in list(hrefs):
        try:
            # go to the href page
            driver.get(href)
            time.sleep(5)

            if len(driver.find_elements(By.CSS_SELECTOR, 'div.js-media-post.clearfix.post.has-tophat')):
                hrefs.remove(href)
                continue

            # open each see more link
            open_see_more_links()

            # get the post data
            get_main_post_data(output_file)

            hrefs.remove(href)

            pickle.dump(hrefs, open('oldposts.dat', 'wb'))

        except:
            continue

    print('Done!')
    driver.quit()


def main():
    # delcare global variable
    global start_year

    # import argparse library
    import argparse

    # start the parser object
    parser = argparse.ArgumentParser(
        description='Scraper for scraping Nextdoor posts'
    )

    # add arguments
    parser.add_argument(
        '-l',
        '--limit',
        help='Number of posts to collect from if there are enough posts available; None == Retrieve all posts available within the given arguments',
        type=int,
        default=None
    )

    parser.add_argument(
        '-sy',
        '--start_year',
        help='Furthest date to go back to for collection; Format: YYYY; None == Retrieve available posts no matter the date',
        type=str,
        default=None
    )

    parser.add_argument(
        '-u',
        '--username',
        help='Nextdoor username for login',
        type=str,
        required=True
    )

    parser.add_argument(
        '-p',
        '--password',
        help='Nextdoor password for login',
        type=str,
        required=True
    )

    parser.add_argument(
        '-k',
        '--keywords_file',
        help='File path where list of keywords is stored in .txt form',
        type=str,
        required=True
    )

    parser.add_argument(
        '-o',
        '--output_file',
        help='File path where output file will be stored in .tsv form',
        type=str,
        required=True
    )

    args = parser.parse_args()

    # assign the start date given
    start_year = args.start_year

    # start the nextdoor scraper
    NextdoorScraper(
        args.limit,
        args.username,
        args.password,
        args.keywords_file,
        args.output_file
    )


if __name__ == '__main__':
    main()
