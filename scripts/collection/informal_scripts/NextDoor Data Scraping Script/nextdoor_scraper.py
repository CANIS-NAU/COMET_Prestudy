from logging import exception
from pydoc import classname
from debugpy import configure
from jmespath import search
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, requests, random, pandas as pd, datetime, calendar
from datetime import datetime as dt
from dateutil.relativedelta import *
from os.path import exists

start_date = None
MONTHS = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

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

def create_output_file(output_file: str):
    """Create the tsv file that will be used to store data

    Parameters
    ----------
    output_file : str
        The tsv file name and file path that holds all of the scraped data from Nextdoor
    """

    # create pandas dataframe as a tsv file and create the file in the specified location given
    dataframe = pd.DataFrame(columns = ['post_id', 'author', 'neighborhood', 'date', 'text', 'posted_in', 'media_list', 'num_of_comments', 'who_commented', 'comment_ids', 'num_of_reactions', 'reactions'])
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
        break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(5)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height

def get_date(date: str):
    """Make sure that the post date is within date limits and
    create the correct date format for the given date

    Parameters
    ----------
    date : str
        The post date given on the website

    Returns
    ----------
    str
        A string of the date in the correct format
    
    True
        The True literal as a sign that the post should be removed from the list of posts
    
    None
        Nothing as a sign that the post should be used or there is no correct format date
    """

    global start_date

    # import re library
    import re

    # if the date is in minutes
    if 'min ago' in date or 'min' in date:
        difference = date.split(' ')[0]
        difference = int(difference)
        post_date = dt.now() - datetime.timedelta(minutes = difference)

        # if the date is earlier than the given start date
        if start_date != None:
            if post_date < start_date:
                return True

        return str(post_date.date())
    
    #if the date is in hours
    elif 'hr ago' in date or 'hr' in date:
        difference = date.split(' ')[0]
        difference = int(difference)
        post_date = dt.now() - datetime.timedelta(hours = difference)

        # if the date is earlier than the given start date
        if start_date != None:
            if post_date < start_date:
                return True

        return str(post_date.date())
    
    # if the date is days ago
    elif 'days ago' in date or 'day ago' in date or 'day' in date:
        difference = date.split(' ')[0]
        difference = int(difference)
        post_date = dt.today() - datetime.timedelta(days = difference)

        # if the date is earlier than the given start date
        if start_date != None:
            if post_date < start_date:
                return True

        return str(post_date.date())

    # if the date is weeks ago
    elif 'weeks ago' in date:
        difference = date.split(' ')[0]
        difference = int(difference)
        post_date = dt.today() + relativedelta(weeks=-difference)

        # if the date is earlier than the given start date
        if start_date != None:
            if post_date < start_date:
                return True

        return str(post_date.date())

    # if the date is an actual date, ex: '12 Jun' or '1 May 19'
    else:

        # if the date is one digit, ex: '16w'
        if len(date.split(' ')) == 1:
            date = re.split('(\d+)', date)

            # if the date is in week form
            if 'w' in date:
                difference = date[1]
                difference = int(difference)
                post_date = dt.today() + relativedelta(weeks=-difference)

                # if the date is earlier than the given start date
                if start_date != None:
                    if post_date < start_date:
                        return True

                return str(post_date.date())

        # if the date can be split in two, ex: '16 Apr'
        if len(date.split(' ')) == 2:
            strings = list(MONTHS.keys())
            nums = list(MONTHS.values())

            # if the date month is later than the current month, ex: current month is May and date month is July
            # the date is then last year, check to be sure it is in range
            if strings.index(date.split(' ')[1]) > nums.index(dt.now().month):
                current_year = dt.today().year
                post_date = dt(current_year, MONTHS[date.split(' ')[1]], int(date.split(' ')[0])) + relativedelta(years=-1)
                post_date = post_date.date()

                # if the date is earlier than the given start date
                if start_date != None:
                    if post_date > start_date.date():
                        return True

                return str(post_date)

            # if the month is current, make sure the date is not later than the current date
            # the date is then last year, check to be sure it is in range
            if strings.index(date.split(' ')[1]) == nums.index(dt.now().month):
                post_day = date.split(' ')[0]

                if int(post_day) > dt.now().day:
                    current_year = dt.today().year
                    post_date = dt(current_year, MONTHS[date.split(' ')[1]], int(date.split(' ')[0])) + relativedelta(years=-1)
                    post_date = post_date.date()

                    # if the date is earlier than the given start date
                    if start_date != None:
                        if post_date > start_date.date():
                            return True

                    return str(post_date)
            
            # otherwise, the date is in range
            else:
                current_year = dt.today().year
                post_date = dt(current_year, MONTHS[date.split(' ')[1]], int(date.split(' ')[0]))
                post_date = post_date.date()

                return str(post_date)

        # if the date can be split in 3, ex: '12 Jun 19' or '18 May 20'
        # split the date correctly
        if len(date.split(' ') == 3):
            post_day = date.split(' ')[0]
            post_month = date.split(' ')[1]
            post_year = date.split(' ')[2]
            
            post_month = MONTHS[post_month]

            post_year = '20' + post_year
             
            post_date = dt(int(post_year), post_month, int(post_day))

            # if the date is earlier than the given start date
            if start_date != None:
                if post_date > start_date.date():
                    return True

            return str(post_date.date())
    
    return None

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

def get_comment_ids():
    """Get the comment ids of the comments of the post

    Returns
    ----------
    comment_ids : list
        A list of comment ids from the post
    """

    # get the number of comments and create the comment ids
    comment_ids = len(driver.find_elements(By.CSS_SELECTOR, 'div.js-media-comment'))
    comment_ids = [str(post_id) + '_' + str(num) for num in range(1, comment_ids+1)]
    return comment_ids

def get_reactions(post : object, type : str):
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
        reactions_button = post.find_elements(By.CSS_SELECTOR, 'button._1p1i18kz.post-action-count-container-reaction-count.post-action-space-if-not-last-child._15-DWJ4U.button-text')
    elif type == 'comment':
        reactions_button = post.find_elements(By.CSS_SELECTOR, 'button._1p1i18kz._15-DWJ4U.button-text')

    
    # if a reactions button does exist
    # click on the button and gather each reaction and who did that reaction
    if len(reactions_button) > 0:
        driver.execute_script("arguments[0].click();", reactions_button[0])
        time.sleep(random.randint(2, 5))

        who_reacted = driver.find_elements(By.CSS_SELECTOR, 'h2.css-up964u')
        who_reacted = [name.text for name in who_reacted]

        reaction_divs = driver.find_elements(By.CSS_SELECTOR, 'div.css-clcwj9')
        reactions = {'Like': [], 'Thank': [], 'Agree': [], 'Haha': [], 'Wow': [], 'Sad': []}
        for reaction in reaction_divs:
            reaction_img = reaction.find_elements(By.CSS_SELECTOR, 'img')[1].get_attribute('alt')
            reaction_person = reaction.find_element(By.CSS_SELECTOR, 'h2.css-up964u').text

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
        exit_button = driver.find_element(By.CSS_SELECTOR, 'div.css-5qiylr').find_element(By.CSS_SELECTOR, 'div.css-dkr4zn')
        driver.execute_script("arguments[0].click();", exit_button)
        time.sleep(random.randint(2, 5))

        # return the reactions
        return reactions

    # otherwise, there are no reactions
    else:

        # return nothing, since there are no reactions
        return None  

def upload_data(data : list, output_file: str):
    """Add the row of data to the given output file

    Parameters
    ----------
    data : list
        Dictionary of data
    
    output_file : str
        The output file given in the arguments
    """

    df = pd.DataFrame(data)
    df.to_csv(output_file, mode = 'a', sep='\t', header=False)

def get_comment_data(output_file):
    """Gathers the data of each comment of a post

    Parameters
    ----------
    output_file : str
        The output file given in the arguments
    """

    # get the comments of the post
    comments = driver.find_elements(By.CSS_SELECTOR, 'div.js-media-comment')

    # count the comments
    comment_id = 1

    # loop through each comment and gather its data
    for comment in comments:
        parent_element = comment.find_element(By.XPATH, '..')
        data = [{
            'post_id' : str(post_id) + '_' + str(comment_id),
            'author' : comment.find_elements(By.CSS_SELECTOR, 'a.comment-detail-author-name')[0].text if len(comment.find_elements(By.CSS_SELECTOR, 'a.comment-detail-author-name')) > 0 else None,
            'neighborhood' : comment.find_elements(By.CSS_SELECTOR, 'a.PH4qbR1K')[0].text if len(comment.find_elements(By.CSS_SELECTOR, 'a.PH4qbR1K')) > 0 else None,
            'date' : get_date(comment.find_elements(By.CSS_SELECTOR, 'span.css-ra9tcg')[0].text) if len(comment.find_elements(By.CSS_SELECTOR, 'span.css-ra9tcg')) > 0 else None,
            'text' : comment.find_elements(By.CSS_SELECTOR, 'span.Linkify')[0].text if len(comment.find_elements(By.CSS_SELECTOR, 'span.Linkify')) > 0 else None,
            'posted in' : main_post.find_elements(By.CSS_SELECTOR, 'div.css-m9gd8r')[0].text if len(main_post.find_elements(By.CSS_SELECTOR, 'div.css-m9gd8r')) > 0 else None,
            'media list' : get_post_media(comment) if get_post_media(comment) != [] else None,
            'who commented' : list(set([name.text for name in parent_element.find_elements(By.CSS_SELECTOR, 'a.comment-detail-author-name')[1:]])) if len(parent_element.find_elements(By.CSS_SELECTOR, 'a.comment-detail-author-name')) > 1 else None,
            'comment ids' : [str(post_id) + '_' + str(num + comment_id) for num in range(1, len(parent_element.find_elements(By.CSS_SELECTOR, 'div.js-media-comment')))] if len(parent_element.find_elements(By.CSS_SELECTOR, 'div.js-media-comment')) > 1 else None,
            'reactions' : get_reactions(comment, 'comment')
        }]

        # increment comment id
        comment_id += 1

        upload_data(data, output_file)

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
    main_post = driver.find_element(By.CSS_SELECTOR, 'div.js-media-post.clearfix.post')

    # gather the data of the main post
    data = [{
        'post_id' : post_id,
        'author' : main_post.find_elements(By.CSS_SELECTOR, 'a._1QrCPIoo._2nXsqARR')[0].text if len(main_post.find_elements(By.CSS_SELECTOR, 'a._1QrCPIoo._2nXsqARR')) > 0 else None,
        'neighborhood' : main_post.find_elements(By.CSS_SELECTOR, 'a.post-byline-redesign')[0].text if len(main_post.find_elements(By.CSS_SELECTOR, 'a.post-byline-redesign')) > 0 else None, 
        'date' : get_date(main_post.find_elements(By.CSS_SELECTOR, 'a.post-byline-redesign')[1].text) if len(main_post.find_elements(By.CSS_SELECTOR, 'a.post-byline-redesign')) > 0 else None,
        'text' : main_post.find_elements(By.CSS_SELECTOR, 'span.Linkify')[0].text if len(main_post.find_elements(By.CSS_SELECTOR, 'span.Linkify')) > 0 else None,
        'posted in': main_post.find_elements(By.CSS_SELECTOR, 'div.css-m9gd8r')[0].text if len(main_post.find_elements(By.CSS_SELECTOR, 'div.css-m9gd8r')) > 0 else None,
        'media list' : get_post_media(main_post) if get_post_media(main_post) != [] else None,
        'who commented' : list(set([name.text for name in driver.find_elements(By.CSS_SELECTOR, 'div.css-66amwq')])) if len(driver.find_elements(By.CSS_SELECTOR, 'div.css-66amwq')) > 0 else None,
        'comment ids' : get_comment_ids() if get_comment_ids() != [] else None,
        'reactions' : get_reactions(main_post, 'post')
    }]

    upload_data(data, output_file)

def open_see_more_links():
    """Open all of the 'see more' links on the page
    """

    # find all of the see more buttons
    see_more_buttons = driver.find_elements(By.CSS_SELECTOR, 'button.see-previous-comments-button-paged._1eW-tOzA')

    # while see more buttons exist
    while len(see_more_buttons) > 0:

        # open them
        driver.execute_script("arguments[0].click();", see_more_buttons[0])
        time.sleep(random.randint(2, 5))

        # check for more
        see_more_buttons = driver.find_elements(By.CSS_SELECTOR, 'button.see-previous-comments-button-paged._1eW-tOzA')

def NextdoorScraper(limit, username, password, keywords_file, output_file, chromedriver):
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
    global driver, post_id, start_date

    # configure the driver
    driver = configure_driver(chromedriver)

    # create the output file
    create_output_file(output_file)

    # create the keyword string
    keyword_string = create_keyword_string(keywords_file)

    # login to nextdoor
    login(username, password)

    # search for the given keyword posts
    driver.get('https://nextdoor.com/search/posts/?ccid=7E25E89B-7923-4364-A11B-20E127E181E1&navigationScreen=FEED&ssid=BC6802A2-6432-4887-884E-789810B2F4E2&query=' + keyword_string)
    time.sleep(5)

    # scroll through the entire page
    scroll_page()

    # get the posts shown
    posts = driver.find_elements(By.CSS_SELECTOR, 'a._2pCkWHax.css-1q9s7yp')

    # if there is a start date
    # check the dates of each post
    # if the post is earlier than the given start date
    # remove it from the posts list
    if start_date != None:
        print(start_date)
        start_date = dt.strptime(start_date, '%m/%Y')
        print(start_date)

        for post in posts:
            date = [date.text.split('·')[1] for date in post.find_elements(By.CSS_SELECTOR, 'div.css-77j1dk') if '·' in date.text][0].strip()
            if get_date(date):
                posts.remove(post) 

    # if there is a limit
    # only get the limit number of posts
    if limit != None:
        if limit < len(posts):
            posts = posts[0:limit]

    # if there are no posts
    # let the user know and quit
    if len(posts) == 0:
        print('No posts were found with the arguments given.')
        quit()

    # start a variable of hrefs
    hrefs = []

    # loop through each post and get their hrefs
    for post in posts:
        href = post.get_attribute('href')
        hrefs.append(href)

    # start the post id counting
    post_id = 1

    # loop through each href
    for href in hrefs:

        # go to the href page
        driver.get(href)
        time.sleep(5)

        # open each see more link
        open_see_more_links()

        # get the main post data
        get_main_post_data(output_file)

        # get the posts comment data
        get_comment_data(output_file)

        # increment to the next post id
        post_id += 1

def main():
    # delcare global variable
    global start_date

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
        '-sd',
        '--start_date',
        help='Furthest date to go back to for collection; Format: MM/YYYY; None == Retrieve available posts no matter the date',
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

    parser.add_argument(
        '-d',
        '--chromedriver',
        help='File path where chromedriver is stored',
        type=str,
        required=True
    )

    args = parser.parse_args()

    # assign the start date given
    start_date = args.start_date

    # start the nextdoor scraper
    NextdoorScraper(
        args.limit, 
        args.username, 
        args.password, 
        args.keywords_file, 
        args.output_file,
        args.chromedriver
        )

if __name__ == '__main__':
    main()