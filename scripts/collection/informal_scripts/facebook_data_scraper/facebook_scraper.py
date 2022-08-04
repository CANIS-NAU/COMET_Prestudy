from jmespath import search
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import time
import random
import pandas as pd
import pickle
import os
import string
from dateutil.relativedelta import *
from datetime import date
from os.path import exists
from selenium.webdriver.support.expected_conditions import *

FACEBOOK_YEARS = {'2022': '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAyMlxcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAyMi0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDIyXFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAyMi0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMjItMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMjItMTItMzFcXFwifVwifSJ9', '2021': '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAyMVxcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAyMS0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDIxXFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAyMS0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMjEtMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMjEtMTItMzFcXFwifVwifSJ9', '2020': '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAyMFxcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAyMC0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDIwXFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAyMC0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMjAtMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMjAtMTItMzFcXFwifVwifSJ9',
                  '2019': '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAxOVxcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAxOS0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDE5XFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAxOS0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMTktMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMTktMTItMzFcXFwifVwifSJ9', '2018': '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAxOFxcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAxOC0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDE4XFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAxOC0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMTgtMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMTgtMTItMzFcXFwifVwifSJ9', '2017': '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAxN1xcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAxNy0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDE3XFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAxNy0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMTctMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMTctMTItMzFcXFwifVwifSJ9'}

current_group_page = None
past_data = []

driver = None

def configure_driver():
    global driver

    # configure webdriver
    driver = webdriver.Safari()


def create_output_file(output_file: str):
    """Create the tsv file that will be used to store data

    Args:
        output_file (str): The tsv file name and file path that holds all of the scraped data from Nextdoor
    """

    # create pandas dataframe as a tsv file and create the file in the specified location given
    dataframe = pd.DataFrame(columns=['group or page', 'author', 'date', 'text', 'media', 'comments',
                             '# comments', '# reactions', '# shares'])
    dataframe.to_csv(output_file, sep='\t')


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


def upload_data(data: list, output_file: str):
    """Adds the row of data to the given output file 

    Args:
        data (list): Dictionary of page or comment data
        output_file (str):The output file name given in the arguments
    """

    df = pd.DataFrame(data)
    df.to_csv(output_file, mode='a', sep='\t', header=False, index=True)


def get_keyword_list(keywords_file: str) -> list:
    """Creates a list of keywords

    Args:
        keywords_file (str): File path where list of keywords is stored in .txt form

    Returns:
        list: A list where each element is a keyword from the given keywords file
    """

    # declare keywords list and open the keywords file to read
    keywords = []
    keywords_file = open(keywords_file, 'r')

    # loop through each line in the keywords file
    # append each keyword (line) to the keywords list
    for keyword in keywords_file:
        keyword = keyword.replace('\n', '')
        keywords.append(keyword)

    # return the keywords list
    return keywords


def login(username: str, password: str):
    """Logs user into Facebook

    Args:
        username (str): User's facebook username
        password (str): User's facebook password
    """

    # go to facebook
    driver.get('https://www.facebook.com/')

    # insert the username
    username_input = driver.find_element(
        By.CSS_SELECTOR, 'input.inputtext._55r1._6luy')
    username_input.send_keys(username)

    # insert the password
    password_input = driver.find_element(
        By.CSS_SELECTOR, 'input.inputtext._55r1._6luy._9npi')
    password_input.send_keys(password)

    # log in
    log_in_button = driver.find_element(
        By.CSS_SELECTOR, 'button._42ft._4jy0._6lth._4jy6._4jy1.selected._51sy')
    driver.execute_script("arguments[0].click();", log_in_button)
    time.sleep(random.randint(2, 5))


def get_id_list(ids: str) -> list:
    """Creates a list from the string provided

    Args:
        ids (str): A string of either group ids or string ids

    Returns:
        list: A list of either group ids or string ids
    """

    # strip and split ids string
    ids = ids.strip()
    ids = ids.split(',')

    # return the ids list
    return ids


def get_dates_list(start_year: str) -> list:
    """Creates a list of facebook filters that correlate to the given start date and on

    Args:
        start_year (str): The start date that the user would like to begin looking for data

    Returns:
        list: The list of filters that correlate to years, starting at the start date year
    """

    # initialize the list of date filters
    dates = []

    # if the year given is in the FACEBOOK_YEARS dictionary
    if start_year in FACEBOOK_YEARS:

        # match the year to the filter
        keys = list(FACEBOOK_YEARS.keys())
        index = keys.index(start_year)

        while index >= 0:

            dates.append(list(FACEBOOK_YEARS.values())[index])
            index = index - 1

    # otherwise, let the user know that the date doesn't exist in the code
    # let the user know where they can add the date and filter
    # quit the program
    else:

        print('\nThe year provided does not have an equivalent filter. Please add the year and filter to the FACEBOOK_YEARS dictionary at line 13.')
        driver.quit()

    # return the date filters gathered
    return dates


def get_author(post: object, post_type: str) -> str | None:
    """Retrieves the name of the author that wrote the post/comment

    Args:
        post (object): The WebElement object that represents a post or comment
        post_type (str): Either 'post' or 'comment', allows for correct element searching

    Returns:
        str | None: The author's name if it was found, otherwise None
    """

    # if the post type is a post
    if post_type == 'post':

        # get the author name element
        author = post.find_elements(
            By.CSS_SELECTOR, 'a.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gpro0wi8.oo9gr5id.lrazzd5p')

        # make sure elements exist
        if len(author) > 0:

            # get the text and return the author's name
            author = author[0].text
            return author

        # otherwise, return None
        else:

            return None

    # if the post type is a comment
    elif post_type == 'comment':

        # get the author name element
        author = post.find_elements(
            By.CSS_SELECTOR, 'span.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.lr9zc1uh.a8c37x1j.fe6kdd0r.mau55g9w.c8b282yb.keod5gw0.nxhoafnm.aigsh9s9.d9wwppkn.mdeji52x.e9vueds3.j5wam9gi.lrazzd5p.oo9gr5id')

        # make sure elements exist
        if len(author) > 0:

            # get the text and return the author's name
            author = author[0].text
            return author

        # otherwise, return None
        else:

            return None


def get_date(post: object, post_type: str) -> str | None:
    """Finds the date of the post/comment

    Args:
        post (object): The WebElement object that represents a post or comment
        post_type (str): Either 'post' or 'comment', allows for correct element searching

    Returns:
        str | None: The comment/post date if it was found, otherwise None
    """

    # if the post type is a post
    if post_type == 'post':

        # find the date element
        date_elements = post.find_elements(
            By.CSS_SELECTOR, 'span.j1lvzwm4.stjgntxs.ni8dbmo4.q9uorilb.gpro0wi8')

        # if a date element exists
        # get the label, find the reference, and return the innerHTML (the date shown)
        if len(date_elements) > 0:

            date_elements = date_elements[0]
            date_label = date_elements.get_attribute('aria-labelledby')
            date_references = driver.find_elements(By.ID, date_label)

            if len(date_references) > 0:

                date = date_references[0].get_attribute('innerHTML')
                return date

            # otherwise, return None
            else:

                return None

        # otherwise, return None
        else:

            return None

    # if the post type is a comment
    elif post_type == 'comment':

        # find the date element
        date_elements = post.find_elements(
            By.CSS_SELECTOR, 'a.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gpro0wi8.m9osqain.knj5qynh')

        # if a date element exists
        # get the text of the element and return the text
        if len(date_elements) > 0:

            date = date_elements[0].text
            return date

        # otherwise, return None
        else:

            return None


def get_text(post: object, post_type: str) -> str:
    """Retrieves the text from the provided comment or post

    Args:
        post (object): The WebElement object that represents a post or comment
        post_type (str): Either 'post' or 'comment', allows for correct element searching

    Returns:
        str: The text of the given comment or post
    """

    # if the post type is a post
    # find the text element and return it
    if post_type == 'post':

        text = post.find_elements(
            By.CSS_SELECTOR, 'div.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.c1et5uql')

        if len(text) > 0:

            text = text[0].text
            return text

        # otherwise, return None
        else:

            return None

    # if the post type is a comment
    # find the text element and return it
    elif post_type == 'comment':

        text = post.find_elements(
            By.CSS_SELECTOR, 'div.ecm0bbzt.e5nlhep0.a8c37x1j')

        if len(text) > 0:

            text = text[0].text
            return text

        # otherwise return None
        else:

            return None


def open_see_more_links():
    """Opens all 'see more' links within the page to read all text available 
    """

    # find all of the 'see more' link elements
    links = driver.find_elements(
        By.CSS_SELECTOR, 'div.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gpro0wi8.oo9gr5id.lrazzd5p')

    # while 'see more' link elements exist
    while True:

        try:
            # initialize counter to keep track of 'see more' elements
            # specifically because some other elements use the same class
            see_more_counter = 0

            # loop through eack link
            for link in links:

                # if the text of the link says see more
                # increment the counter
                # click on the link to open more text
                if link.text == 'See more':

                    see_more_counter += 1
                    driver.execute_script("arguments[0].click();", link)
                    time.sleep(random.randint(2, 5))

            # if the see more counter is 0, break the loop since there are no more see more links
            if see_more_counter == 0:
                break

            # if the see more counter is more than 0
            # there is a possibility of more see more links popping up when opening previous ones
            # look for more links and loop again
            links = driver.find_elements(
                By.CSS_SELECTOR, 'div.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gpro0wi8.oo9gr5id.lrazzd5p')

        except:

            # if the see more counter is more than 0
            # there is a possibility of more see more links popping up when opening previous ones
            # look for more links and loop again
            links = driver.find_elements(
                By.CSS_SELECTOR, 'div.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gpro0wi8.oo9gr5id.lrazzd5p')

            continue


def scroll_reaction_box():

    scroll_bar = driver.find_elements(
        By.CSS_SELECTOR, 'div.rpm2j7zs.k7i0oixp.gvuykj2m.j83agx80.cbu4d94t.ni8dbmo4.du4w35lb.q5bimw55.ofs802cu.pohlnb88.dkue75c7.mb9wzai9.l56l04vs.r57mb794.l9j0dhe7.kh7kg01d.eg9m0zos.c3g1iek1.otl40fxz.cxgpxx05.rz4wbd8a.sj5x9vvc.a8nywdso')

    if len(scroll_bar) > 0:

        # get the height of the web page
        last_height = driver.execute_script(
            'return arguments[0].scrollHeight', scroll_bar)

        # scroll while the end of the page hasn't been reached
        while True:

            try:

                driver.execute_script(
                    "arguments[0].scrollTo(0, arguments[0].scrollHeight)", scroll_bar)
                time.sleep(5)

                new_height = driver.execute_script(
                    'return arguments[0].scrollHeight', scroll_bar)

                if new_height == last_height:

                    break

                last_height = new_height

            except:

                break


def get_media(post: object, post_type: str) -> list:
    """Retrieves a list of media sources from the provided comment or post

    Args:
        post (object): The WebElement object that represents a post or comment
        post_type (str): Either 'post' or 'comment', allows for correct element searching

    Returns:
        list: Media sources from the provided comment or post
    """

    # if the post type is a post
    # gather the media elements
    # initialize the media variable
    if post_type == 'post':

        media_elements = post.find_elements(
            By.CSS_SELECTOR, '.i09qtzwb.n7fi1qx3.datstx6m.pmk7jnqg.j9ispegn.kr520xx4.k4urcfbm')
        media = []

        # if media elements exist
        # loop through each media element
        if len(media_elements) > 0:

            for media_element in media_elements:

                # if the media element has a source
                # append the source to the media list
                if media_element.get_attribute('src') != None:

                    if media_element.get_attribute('src').startswith('http'):

                        media.append(media_element.get_attribute('src'))

                # check if video elements exist
                video_elements = media_element.find_elements(
                    By.CSS_SELECTOR, 'video')

                # if video elements exist
                # loop through the video elements
                # append the video element source to the media list
                if len(video_elements) > 0:

                    for video_element in video_elements:

                        if video_element.get_attribute('src').startswith('http'):

                            media.append(video_element.get_attribute('src'))

        # if the media list contains sources
        # return the list
        if len(media) > 0:

            return media

        # otherwise, return None
        else:

            return None

    # if the post type is a comment
    # get the media elements
    # initialize the media list
    elif post_type == 'comment':

        media_elements = post.find_elements(
            By.CSS_SELECTOR, 'div.j83agx80.bvz0fpym.c1et5uql')
        media = []

        # if media elements exist
        # loop through each media element
        # find images
        # loop through images
        # append image sources to the media list
        # do the same for videos
        if len(media_elements) > 0:

            for media_element in media_elements:

                image_elements = media_element.find_elements(
                    By.CSS_SELECTOR, 'img')

                for image_element in image_elements:

                    if image_element.get_attribute('src').startswith('http'):

                        media.append(image_element.get_attribute('src'))

                video_elements = media_element.find_elements(
                    By.CSS_SELECTOR, 'video')

                for video_element in video_elements:

                    if video_element.get_attribute('src').startswith('http'):

                        media.append(video_element.get_attribute('src'))

        # if the media list has sources in it
        # return the list
        if len(media) > 0:

            return media

        # otherwise, return None
        else:

            return None


def get_num_comments(post: object) -> str:
    """Retrieved the number of comments for a post

    Args:
        post (object): The WebElement object that represents a post

    Returns:
        str: The number of comments from the post provided
    """

    # find the comment elements in the post
    comment_elements = post.find_elements(
        By.CSS_SELECTOR, 'span.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.lr9zc1uh.a8c37x1j.fe6kdd0r.mau55g9w.c8b282yb.keod5gw0.nxhoafnm.aigsh9s9.d3f4x2em.iv3no6db.jq4qci2q.a3bd9o3v.b1v8xokw.m9osqain')

    # initialize the number of comments variable
    num_comments = None

    # if comment elements exist
    # loop through each comment element
    if len(comment_elements) > 0:

        for comment_element in comment_elements:

            # if the comment element has the words Comment or Comments within the text
            # split the text in two by a space and grab the first list element (the number of comments)
            # return the number of comments
            if 'Comment' in comment_element.text or 'Comments' in comment_element.text:

                num_comments = comment_element.text.split(' ')[0]

                return num_comments

    # otherwise, return None
    return num_comments


def get_num_reactions(post: object, post_type: str) -> str:
    """Retrieves the number of reactions on a post or comment

    Args:
        post (object): The WebElement object that represents a post or comment
        post_type (str): Either 'post' or 'comment', allows for correct element searching

    Returns:
        str: The number of reactions on the comment or post
    """

    # if the post type is a post
    # find the reaction elements of the post
    if post_type == 'post':

        reactions_element = post.find_elements(
            By.CSS_SELECTOR, 'span.pcp91wgn')

        # if reaction elements exist
        # get the reaction element's text (the num of reactions)
        # return the number of reactions
        if len(reactions_element) > 0:

            num_reactions = reactions_element[0].text

            return num_reactions

        # otherwise, return None
        else:

            return None


def get_num_shares(post: object) -> str:
    """Retrieve the number of shares of a post

    Args:
        post (object): The WebElement object that represents a post or comment

    Returns:
        str: The number of shares of the provided post
    """

    # gather the share elements of the post
    share_elements = post.find_elements(
        By.CSS_SELECTOR, 'span.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.lr9zc1uh.a8c37x1j.fe6kdd0r.mau55g9w.c8b282yb.keod5gw0.nxhoafnm.aigsh9s9.d3f4x2em.iv3no6db.jq4qci2q.a3bd9o3v.b1v8xokw.m9osqain')

    # initialize the number of shares to None
    num_shares = None

    # if share elements exist
    # loop through each share element
    if len(share_elements) > 0:

        for share_element in share_elements:

            # if the share element has the word share or shares in the text
            # get the number of shares from the element's text
            # return the number of shares
            if 'Share' in share_element.text or 'Shares' in share_element.text:

                num_shares = share_element.text.split(' ')[0]
                return num_shares

    # otherwise, return None
    return num_shares


def open_comments(post: object):
    """Clicks on the comments links to open all of the comments of a post

    Args:
        post (object): The WebElement object that represents a post
    """

    # get the post's comment elements
    comment_elements = post.find_elements(By.CSS_SELECTOR, 'div.oajrlxb2.gs1a9yip.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.nhd2j8a9.mg4g778l.pfnyh3mw.p7hjln8o.tgvbjcpo.hpfvmrgz.esuyzwwr.f1sip0of.n00je7tq.arfg74bv.qs9ysxi8.k77z8yql.pq6dq46d.btwxx1t3.abiwlrkh.lzcic4wl.dwo3fsh8.g5ia77u1.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.gmql0nx0.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.du4w35lb.gpro0wi8')

    # if comment elements exist
    # loop through each comment element
    if len(comment_elements) > 0:

        for comment_element in comment_elements:

            # if the comment element has the word comment or comments in the text
            # click on the element and break
            if 'Comment' in comment_element.text or 'Comments' in comment_element.text:

                driver.execute_script("arguments[0].click();", comment_element)
                time.sleep(random.randint(2, 5))

                break


def get_all_comments(post: object):
    """If the choice is available, chooses to see all comments rather than top comments or most recent comments

    Args:
        post (object): The WebElement object that represents a post
    """

    # find all most recent dropdown elements
    most_recent_elements = post.find_elements(
        By.CSS_SELECTOR, 'div.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.n00je7tq.arfg74bv.qs9ysxi8.k77z8yql.l9j0dhe7.abiwlrkh.p8dawk7l.lzcic4wl')

    # if those elements exist
    # loop through each element
    if len(most_recent_elements) > 0:

        for most_recent_element in most_recent_elements:

            # if the words most recent or top comments are in the most recent element text
            # click the element
            # find the all comment element option
            # click the all comments option
            if 'Most recent' in most_recent_element.text or 'Top comments' in most_recent_element.text:

                driver.execute_script(
                    "arguments[0].click();", most_recent_element)
                time.sleep(random.randint(2, 5))

                all_comments_elements = driver.find_elements(
                    By.CSS_SELECTOR, 'div.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.p7hjln8o.esuyzwwr.f1sip0of.n00je7tq.arfg74bv.qs9ysxi8.k77z8yql.abiwlrkh.p8dawk7l.lzcic4wl.dwo3fsh8.rq0escxv.nhd2j8a9.j83agx80.btwxx1t3.pfnyh3mw.opuu4ng7.kj2yoqh6.kvgmc6g5.oygrvhab.pybr56ya.dflh9lhu.f10w8fjw.scb9dxdr.l9j0dhe7.i1ao9s8h.du4w35lb.bp9cbjyn')

                for all_comments_element in all_comments_elements:

                    if 'All comments' in all_comments_element.text:

                        driver.execute_script(
                            "arguments[0].click();", all_comments_element)
                        time.sleep(random.randint(2, 5))

                        break

                break


def open_all_comments_replies(post: object):
    """Click all reply extenders to see all comments and replies

    Args:
        post (object): The WebElement object that represents a post
    """

    # find all view elements in the post
    view_elements = post.find_elements(By.CSS_SELECTOR, 'div.oajrlxb2.g5ia77u1.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.nhd2j8a9.mg4g778l.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.tgvbjcpo.hpfvmrgz.jb3vyjys.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.esuyzwwr.f1sip0of.du4w35lb.n00je7tq.arfg74bv.qs9ysxi8.k77z8yql.pq6dq46d.btwxx1t3.abiwlrkh.lzcic4wl.bp9cbjyn.m9osqain.buofh1pr.g5gj957u.p8fzw8mz.gpro0wi8')

    # while true
    while True:

        # initialize view element counter
        view_element_counter = 0

        # loop through each view element
        for view_element in view_elements:

            # if the word view or replies is in the view element text
            # increment the view element counter
            # click on the view element
            if 'view' in view_element.text.lower() or 'replies' in view_element.text.lower():

                view_element_counter += 1

                driver.execute_script("arguments[0].click();", view_element)
                time.sleep(random.randint(2, 5))

        # if the counter == 0, break, since there are no more elements to click
        if view_element_counter == 0:

            break

        # otherwise, try to find more and loop again
        view_elements = post.find_elements(By.CSS_SELECTOR, 'div.oajrlxb2.g5ia77u1.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.nhd2j8a9.mg4g778l.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.tgvbjcpo.hpfvmrgz.jb3vyjys.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.esuyzwwr.f1sip0of.du4w35lb.n00je7tq.arfg74bv.qs9ysxi8.k77z8yql.pq6dq46d.btwxx1t3.abiwlrkh.lzcic4wl.bp9cbjyn.m9osqain.buofh1pr.g5gj957u.p8fzw8mz.gpro0wi8')


def get_comment_data(post: object):
    """Retrieves all of the data for each comment within the post provided

    Args:
        post (object): The WebElement object that represents a post or comment
        post_id (int): The id of the post provided
        output_file (str): The path and name of the output file
    """

    # open the comments of the post
    open_comments(post)

    # change most recent to all comments
    get_all_comments(post)

    # open all view more comments/replies
    open_all_comments_replies(post)

    return_comments = []

    # get comments element of the post
    comments = post.find_elements(
        By.CSS_SELECTOR, 'div.rj1gh0hx.buofh1pr.ni8dbmo4.stjgntxs.hv4rvrfc')

    # if the element exists
    # start counting the comment id
    # loop through each comment
    # gather each comment's data
    # upload the data
    # increment the comment id
    if len(comments) > 0:

        for comment in comments:

            data = {
                'group or page': current_group_page,
                'author': get_author(comment, 'comment'),
                'date': get_date(comment, 'comment'),
                'text': get_text(comment, 'comment'),
                'media': get_media(comment, 'comment'),
                'comments': None,
                '# comments': None,
                '# reactions': None,
                '# shares': None
            }

            return_comments.append(data)

    return return_comments


def get_page_data(links: list, limit: int, output_file: str):
    """Retrieves the data from the page (posts, comments, etc)

    Args:
        page_ids (list): List of page ids to go to 
        dates (list): List of date filters to go to
        limit (int): Limit of posts to collect
        keywords (list): List of keywords to search for in the page
        output_file (str): The output file path and name
    """

    # get the global variables for counting purposes
    global post_id
    global limit_count
    global past_data

    for link in list(links):

        # go to the website with the correct page id, keyword, and date
        driver.get(link)
        time.sleep(25)

        get_group_or_page()

        # scroll through the whole page and open all see more links
        scroll_page()
        open_see_more_links()

        # get every facebook post and loop through them
        posts = driver.find_elements(
            By.CSS_SELECTOR, 'div.rq0escxv.l9j0dhe7.du4w35lb.hybvsw6c.io0zqebd.m5lcvass.fbipl8qg.nwvqtn77.k4urcfbm.ni8dbmo4.stjgntxs.sbcfpzgs')

        for post in posts:

            text = get_text(post, 'post')

            if text != None:
            
                if not any(word.lower() in text.lower().split(' ') for word in keywords):
                    continue

                if text in past_data:
                    continue

                else:
                    past_data.append(text)
                    pickle.dump(past_data, open('pastdata.dat', 'wb'))

            # collect the data
            data = [{
                'group or page': current_group_page,
                'author': get_author(post, 'post'),
                'date': get_date(post, 'post'),
                'text': text,
                'media': get_media(post, 'post'),
                'comments': get_comment_data(post) if get_num_comments(post) != None else None,
                '# comments': get_num_comments(post),
                '# reactions': get_num_reactions(post, 'post'),
                '# shares': get_num_shares(post)
            }]

            # upload the data
            upload_data(data, output_file)

            # if there are comments
            # get the comment data
            if get_num_comments(post) != None:
                get_comment_data(post)

            # if there is a limit
            # increment the limit since a new post was added
            if limit != None:
                limit_count += 1

                # if the limit was hit
                # let the user know and quit the program
                if limit_count == limit:
                    print('\nLimit has been hit, all done!')
                    driver.quit()

            # increment post id
            post_id += 1

        links.remove(link)
        pickle.dump(links, open('oldpagesources.dat', 'wb'))


def get_group_or_page() -> str | None:
    """Retrieves the group name that the post resides in
    """
    global current_group_page, saved_post_data

    group_page_elements = driver.find_elements(
        By.CSS_SELECTOR, 'span.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.lr9zc1uh.a8c37x1j.fe6kdd0r.mau55g9w.c8b282yb.keod5gw0.nxhoafnm.aigsh9s9.d9wwppkn.mdeji52x.e9vueds3.j5wam9gi.lrazzd5p.m9osqain.hzawbc8m')

    if len(group_page_elements) > 0:

        group_page_element = group_page_elements[0]
        group_page = group_page_element.text.replace('in ', '')

        if group_page != current_group_page and group_page != '':

            current_group_page = group_page

    else:

        current_group_page = None


def get_group_data(links: list, limit: int, output_file: str):
    """_summary_

    Args:
        group_ids (list): _description_
        dates (list): _description_
        limit (int): _description_
        keywords (list): _description_
        output_file (str): _description_
    """

    # get the global variables for counting purposes
    global limit_count
    global post_id
    global past_data

    # initialize limit count and post id
    limit_count = 0
    post_id = 1

    for link in list(links):

        # go to the correct website of the correct group id, keyword, and date
        driver.get(link)
        time.sleep(25)

        get_group_or_page()

        # scroll through the whole page and open all see more links
        scroll_page()
        open_see_more_links()

        # get every facebook post and loop through them
        posts = driver.find_elements(
            By.CSS_SELECTOR, 'div.rq0escxv.l9j0dhe7.du4w35lb.hybvsw6c.io0zqebd.m5lcvass.fbipl8qg.nwvqtn77.k4urcfbm.ni8dbmo4.stjgntxs.sbcfpzgs')

        for post in posts:

            text = get_text(post, 'post')

            if text:
            
                if not any(word.lower() in text.lower().split(' ') for word in keywords):
                    continue

                if text in past_data:
                    time.sleep(5)
                    continue

                else:
                    past_data.append(text)
                    pickle.dump(past_data, open('pastdata.dat', 'wb'))
            
            else:
                time.sleep(5)
                continue

            # collect the data
            data = [{
                'group or page': current_group_page,
                'author': get_author(post, 'post'),
                'date': get_date(post, 'post'),
                'text': text,
                'media': get_media(post, 'post'),
                'comments': get_comment_data(post) if get_num_comments(post) != None else None,
                '# comments': get_num_comments(post),
                '# reactions': get_num_reactions(post, 'post'),
                '# shares': get_num_shares(post)
            }]

            # upload the data
            upload_data(data, output_file)

            # if there is a limit
            # increment the limit count
            if limit != None:
                limit_count += 1

                # if the limit count is hit
                # let the user know and quit the program
                if limit_count == limit:
                    print('\nLimit has been hit, all done!')
                    driver.quit()

            # increment the post id
            post_id += 1

        links.remove(link)
        pickle.dump(links, open('oldgroupsources.dat', 'wb'))


def get_links(ids: list, keywords: str, dates: list, type: str) -> list:
    """Retrieves a list of links to keep track of what link was last left on if the program breaks or closes by accident.

    Args:
        group_ids (list): The groups to collect data from
        keywords (str): The keywords to find within each group
        dates (list): The dates to find each keyword in the groups

    Returns:
        list: The finalized links to go to for data collecting
    """

    links = []

    for id in ids:

        for date in dates:

            for keyword in keywords:

                if type == 'group':

                    links.append('https://www.facebook.com/groups/' +
                                 id + '/search?q=' + keyword + date)

                elif type == 'page':

                    links.append('https://www.facebook.com/page/' +
                                 id + '/search?q=' + keyword + date)

    return links


def check_for_old_sources():

    if os.path.exists('oldgroupsources.dat'):

        while True:

            print(
                '\nOld group sources have been found from your last run that have not been searched through.')
            print('\nWould you like to continue searching through these group sources?')

            response = input('\nY (yes) or N (no): ')

            if response.lower() == 'y':

                print(
                    '\nThe old group sources has been gathered and will be searched through.')
                print('\nContinuing program.')
                break

            if response.lower() == 'n':

                os.remove('oldgroupsources.dat')
                if os.path.exists('pastdata.dat'):
                    os.remove('pastdata.dat')
                print('\nThe old group sources has been removed.')
                print('\nContinuing program.')
                break

            else:

                print('\nYour response does not match our instructions.')
                print('\nPlease try again.')
                continue

    if os.path.exists('oldpagesources.dat'):

        while True:

            print(
                '\nOld page sources have been found from your last run that have not been searched through.')
            print('\nWould you like to continue searching through these page sources?')

            response = input('\nY (yes) or N (no): ')

            if response.lower() == 'y':

                print(
                    '\nThe old page sources has been gathered and will be searched through.')
                print('\nContinuing program.')
                break

            if response.lower() == 'n':

                os.remove('oldpagesources.dat')

                if os.path.exists('pastdata.dat'):
                    os.remove('pastdata.dat')

                print('\nThe old page sources has been removed.')
                print('\nContinuing program.')
                break

            else:

                print('\nYour response does not match our instructions.')
                print('\nPlease try again.')
                continue


def FacebookScraper(limit: int, start_year: str, username: str, password: str, group_ids: str, page_ids: str, keywords_file: str, output_file: str):
    """A Facebook scraper that collects post and comment data from Facebook groups and pages

    Args:
        limit (int): The number of posts to collect
        start_year (str): The year to start looking for posts
        username (str): The user's Facebook username
        password (str): The user's Facebook password
        group_ids (str): A string of group ids to look for posts and comments in
        page_ids (str): A string of page ids to look for posts and comments in
        keywords_file (str): The path and name of the file that contains all of the keywords
        output_file (str): The path and name of the file that will hold all of the data
        chromedriver (str): The path and name of the chromedriver that will be used to scrape Facebook with
    """

    global keywords, past_data

    check_for_old_sources()

    # create list of keywords
    keywords = get_keyword_list(keywords_file)

    create_output_file(output_file)

    # if a start year exists
    # create a list of date filters to run through
    if start_year != None:

        dates = get_dates_list(start_year)

    # otherwise, use the normal non-dated filter
    else:

        dates = [
            '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9In0%3D']

    configure_driver()

    # login to Facebook
    login(username, password)

    if os.path.exists('oldgroupsources.dat'):

        links = pickle.load(open('oldgroupsources.dat', 'rb'))
        past_data = pickle.load(open('pastdata.dat', 'rb'))
        get_group_data(links, limit, output_file)

    else:

        # if group ids exist
        # create a list
        # get the group data (posts and comments)
        if group_ids != None:

            group_ids = get_id_list(group_ids)
            links = get_links(group_ids, keywords, dates, 'group')
            get_group_data(links, limit, output_file)

    if os.path.exists('oldpagesources.dat'):

        links = pickle.load(open('oldpagesources.dat', 'rb'))
        past_data = pickle.load(open('pastdata.dat'))
        get_page_data(links, limit, output_file)

    else:

        if page_ids != None:

            page_ids = get_id_list(page_ids)
            links = get_links(page_ids, keywords, dates, 'page')
            get_page_data(links, limit, output_file)

    # let the user know the program is finished
    # quit the program
    print('\nAll done!')
    driver.quit()


def main():

    global output_file

    import argparse

    parser = argparse.ArgumentParser(
        description='Scraper for scraping Facebook Group and Facebook Page posts'
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
        '-gi',
        '--group_ids',
        help='List of Facebook Group IDS, ex: "12345678, 91011121314"',
        type=str,
        default=None
    )

    parser.add_argument(
        '-pi',
        '--page_ids',
        help='List of Facebook Page IDS, ex: "12345678, 91011121314"',
        type=str,
        default=None
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
        help='File path where output files will be stored in .tsv form',
        type=str,
        required=True
    )

    args = parser.parse_args()

    output_file = args.output_file

    FacebookScraper(
        args.limit,
        args.start_year,
        args.username,
        args.password,
        args.group_ids,
        args.page_ids,
        args.keywords_file,
        args.output_file
    )


if __name__ == '__main__':
    main()
