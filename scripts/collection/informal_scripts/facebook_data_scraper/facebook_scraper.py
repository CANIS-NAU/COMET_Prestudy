from logging import exception
from pydoc import classname
from debugpy import configure
from jmespath import search
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
import pandas as pd
from dateutil.relativedelta import *
from os.path import exists
from selenium.webdriver.support.expected_conditions import *

FACEBOOK_YEARS = {'2022': '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAyMlxcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAyMi0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDIyXFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAyMi0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMjItMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMjItMTItMzFcXFwifVwifSJ9', '2021': '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAyMVxcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAyMS0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDIxXFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAyMS0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMjEtMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMjEtMTItMzFcXFwifVwifSJ9', '2020': '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAyMFxcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAyMC0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDIwXFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAyMC0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMjAtMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMjAtMTItMzFcXFwifVwifSJ9',
                  '2019': '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAxOVxcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAxOS0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDE5XFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAxOS0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMTktMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMTktMTItMzFcXFwifVwifSJ9', '2018': '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAxOFxcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAxOC0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDE4XFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAxOC0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMTgtMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMTgtMTItMzFcXFwifVwifSJ9', '2017': '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAxN1xcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAxNy0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDE3XFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAxNy0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMTctMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMTctMTItMzFcXFwifVwifSJ9'}
REACTIONS = {'Like': 'https://scontent.xx.fbcdn.net/m1/v/t6/An8TxrncfS4U_evP89c2GTGoBe2r0S9YacO1JWgXsSujyi44y6BPf9kkfnteC4B3wzEXsYS1dwFIG3UcC1c_CnQTTPxJ2zIXeAxTrhL8YV0Sp8quSZo.png?ccb=10-5&oh=00_AT_ZgwNdTjXD_7K6-RzczJMNi-f04kCS-omvqOyrJVoLzg&oe=62B7DB16&_nc_sid=55e238', 'Love': 'https://scontent.xx.fbcdn.net/m1/v/t6/An_gITNN0Ds6xnioTKduC3iqXXKmHcF0TaMvC1o32T--llsYDRmAjtiWFZ4R0stgYTwjHPojz-hShHPtB7jPz6xck8JN3Tg0UaA0OqYOiezH8xJvjrc.png?ccb=10-5&oh=00_AT-8LJiQdlXnXf60ii8b7uVYetHYtzqnq-rLCuH0iSUglA&oe=62B8340A&_nc_sid=55e238', 'Haha': 'https://scontent.xx.fbcdn.net/m1/v/t6/An-THWPVXq6iGcl9m0xpRXz841UFwm90bi1X84tlxOb8AG7h_2L7pTpESZnYZ-V90dtWcspSSm2WT0yqmOIxbs7Ms6rYoZGGCYDIVXAaSAA9l2YWfA.png?ccb=10-5&oh=00_AT8ZfQNGNfTkBZg3SGIcsPO8xvoDPepekk9rOfzWpftcww&oe=62B94D69&_nc_sid=55e238',
             'Wow': 'https://scontent.xx.fbcdn.net/m1/v/t6/An9wqz15qSJBbtkJMsumo0WeMIE_6_MbAVHA1LdiH0PgQ82pe50V_Ey2f1YPiEO4lxTLUrsjaXWUC1bTJ3NKmC9FEw2jDlT2KFDmX_N13xBOjzFU8ws.png?ccb=10-5&oh=00_AT-UxLXpV4c14yN3kvb5F9MEtHoDiJmDsEcr8jI7-dkq8w&oe=62B82BC2&_nc_sid=55e238', 'Sad': 'https://scontent.xx.fbcdn.net/m1/v/t6/An8Y5LK0k-qkMes9nYNV5vHn0mALQUIvZXTKK-xekAdyqSbtBsDEcK0-FCVj5Mb7Ycj3xrItHd6q8iTSOi1VEki42ICqEi72j_mjN03-qgfUiGvWFfy1.png?ccb=10-5&oh=00_AT9YA3lQghs4FHNI3CMjeY4MkB4yQI-gJR06bC6HYbIHXQ&oe=62B7A4E5&_nc_sid=55e238', 'Angry': 'https://scontent.xx.fbcdn.net/m1/v/t6/An8ph2gwH6WsvW6pxuYzGzrW8CdpQXACl5PKb5e3I8yS82dPyO-cHlpZDGDHuNFUBIPS8_rJmr6L5JKI6gpOd6GVgh3sLHS6qMD_fv-qg6FoJAzZC2k.png?ccb=10-5&oh=00_AT-rAe7ljYEk1AJ_q7mUqfuy7vXuH3b9Dn8rMmvsRCzNrA&oe=62B8408C&_nc_sid=55e238'}


def configure_driver(chromedriver: str):
    """Configure the chromedriver

    Args:
        chromedriver (str): File path of the chromedriver in string form

    Returns:
        Webdriver: The configured webdriver
    """

    # configure webdriver
    options = Options()
    options.add_argument('--disable-notifications')
    options.page_load_strategy = 'normal'
    options.add_argument('--disable-site-isolation-trials')

    # return webdriver
    return webdriver.Chrome(options=options, executable_path=chromedriver)


def create_output_file(output_file: str):
    """Create the tsv file that will be used to store data

    Args:
        output_file (str): The tsv file name and file path that holds all of the scraped data from Nextdoor
    """

    # create pandas dataframe as a tsv file and create the file in the specified location given
    dataframe = pd.DataFrame(columns=['post_id', 'author', 'date', 'text', 'media', 'comment_ids',
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
    df.to_csv(output_file, mode='a', sep='\t', header=False)


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

        print('The year provided does not have an equivalent filter. Please add the year and filter to the FACEBOOK_YEARS dictionary at line 13.')
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


def get_reactions(post: object, post_type: str) -> dict:
    """Retrieves a dictionary of possible reactions and names of users that reacted with the certain reactions,
    ex: {'Like': ['Cindy'], 'Love': [], etc.}

    Args:
        post (object): The WebElement object that represents a post or comment
        post_type (str): Either 'post' or 'comment', allows for correct element searching

    Returns:
        dict: The reactions and who made each reaction
    """

    # if the post type is a post
    if post_type == 'post':

        # find the reaction bar
        reaction_bar = post.find_elements(
            By.CSS_SELECTOR, 'div.bp9cbjyn.m9osqain.j83agx80.jq4qci2q.bkfpd7mw.a3bd9o3v.kvgmc6g5.wkznzc2l.oygrvhab.dhix69tm.jktsbyx5.rz4wbd8a.osnr6wyh.a8nywdso.s1tcr66n')

        # if the reaction bar exists
        # find the reactions button
        if len(reaction_bar) > 0:

            reaction_bar = reaction_bar[0]
            reactions_button = reaction_bar.find_elements(
                By.CSS_SELECTOR, 'div.oajrlxb2.gs1a9yip.g5ia77u1.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.nhd2j8a9.mg4g778l.pfnyh3mw.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.tgvbjcpo.hpfvmrgz.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.esuyzwwr.f1sip0of.du4w35lb.n00je7tq.arfg74bv.qs9ysxi8.k77z8yql.pq6dq46d.btwxx1t3.abiwlrkh.p8dawk7l.lzcic4wl')

            # if the reactions button exists
            # click the reactions button
            if len(reactions_button) > 0:

                reactions_button = reactions_button[0]
                driver.execute_script(
                    "arguments[0].click();", reactions_button)
                time.sleep(random.randint(2, 5))

                scroll_bar = driver.find_element(
                    By.CSS_SELECTOR, 'div.rpm2j7zs.k7i0oixp.gvuykj2m.j83agx80.cbu4d94t.ni8dbmo4.du4w35lb.q5bimw55.ofs802cu.pohlnb88.dkue75c7.mb9wzai9.l56l04vs.r57mb794.l9j0dhe7.kh7kg01d.eg9m0zos.c3g1iek1.otl40fxz.cxgpxx05.rz4wbd8a.sj5x9vvc.a8nywdso')

                # get the height of the web page
                last_height = driver.execute_script(
                    'return arguments[0].scrollHeight', scroll_bar)

                # scroll while the end of the page hasn't been reached
                while True:
                    driver.execute_script(
                        "arguments[0].scrollTo(0, arguments[0].scrollHeight)", scroll_bar)
                    time.sleep(5)
                    new_height = driver.execute_script(
                        'return arguments[0].scrollHeight', scroll_bar)
                    if new_height == last_height:
                        break
                    last_height = new_height

                reaction_dict = {'Like': [], 'Love': [],
                                 'Haha': [], 'Wow': [], 'Sad': [], 'Angry': []}

                # find the main reactions box
                reactions_box = driver.find_element(
                    By.CSS_SELECTOR, 'div.rpm2j7zs.k7i0oixp.gvuykj2m.j83agx80.cbu4d94t.ni8dbmo4.du4w35lb.q5bimw55.ofs802cu.pohlnb88.dkue75c7.mb9wzai9.l56l04vs.r57mb794.l9j0dhe7.kh7kg01d.eg9m0zos.c3g1iek1.otl40fxz.cxgpxx05.rz4wbd8a.sj5x9vvc.a8nywdso')

                # find each reaction within the reactions box
                reactions = reactions_box.find_elements(
                    By.CSS_SELECTOR, 'div.ow4ym5g4.auili1gw.rq0escxv.j83agx80.buofh1pr.g5gj957u.i1fnvgqd.oygrvhab.cxmmr5t8.hcukyx3x.kvgmc6g5.hpfvmrgz.qt6c0cv9.jb3vyjys.l9j0dhe7.du4w35lb.bp9cbjyn.btwxx1t3.dflh9lhu.scb9dxdr.nnctdnn4')

                # if reactions exist
                # loop through each reaction
                # find the emoji image of the reaction
                # append the user's name that made the reaction to the correct reaction in the dictionary
                # return the dictionary
                if len(reactions) > 0:

                    for reaction in reactions:

                        emoji = reaction.find_element(
                            By.CSS_SELECTOR, 'img.hu5pjgll.bixrwtb6')

                        reaction_index = list(REACTIONS.values()).index(
                            emoji.get_attribute('src'))

                        reactor = reaction.find_element(
                            By.CSS_SELECTOR, 'a.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gpro0wi8.oo9gr5id.lrazzd5p').text

                        reaction_name = list(REACTIONS.keys())[reaction_index]

                        reaction_dict[reaction_name].append(reactor)

                    exit_button = driver.find_element(
                        By.CSS_SELECTOR, 'div.oajrlxb2.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.nhd2j8a9.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.i1ao9s8h.esuyzwwr.f1sip0of.abiwlrkh.p8dawk7l.lzcic4wl.bp9cbjyn.s45kfl79.emlxlaya.bkmhp75w.spb7xbtv.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.j83agx80.taijpn5t.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.tv7at329.thwo4zme.tdjehn4e')
                    driver.execute_script("arguments[0].click();", exit_button)
                    time.sleep(random.randint(2, 5))

                    return reaction_dict

                # otherwise, return None...
                else:

                    return None

            else:

                return None

        else:

            return None

    # if the post type is a comment
    # find the reactions button
    elif post_type == 'comment':

        reactions_button = post.find_elements(
            By.CSS_SELECTOR, 'div.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.n00je7tq.arfg74bv.qs9ysxi8.k77z8yql.l9j0dhe7.abiwlrkh.p8dawk7l.lzcic4wl')

        # if the reactions button exists
        # click the button
        # find the reactions box and each individual reaction
        if len(reactions_button) > 0:

            reactions_button = reactions_button[0]

            driver.execute_script("arguments[0].click();", reactions_button)
            time.sleep(random.randint(2, 5))

            scroll_bar = driver.find_element(
                By.CSS_SELECTOR, 'div.rpm2j7zs.k7i0oixp.gvuykj2m.j83agx80.cbu4d94t.ni8dbmo4.du4w35lb.q5bimw55.ofs802cu.pohlnb88.dkue75c7.mb9wzai9.l56l04vs.r57mb794.l9j0dhe7.kh7kg01d.eg9m0zos.c3g1iek1.otl40fxz.cxgpxx05.rz4wbd8a.sj5x9vvc.a8nywdso')

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

                    scroll_bar = driver.find_element(
                        By.CSS_SELECTOR, 'div.rpm2j7zs.k7i0oixp.gvuykj2m.j83agx80.cbu4d94t.ni8dbmo4.du4w35lb.q5bimw55.ofs802cu.pohlnb88.dkue75c7.mb9wzai9.l56l04vs.r57mb794.l9j0dhe7.kh7kg01d.eg9m0zos.c3g1iek1.otl40fxz.cxgpxx05.rz4wbd8a.sj5x9vvc.a8nywdso')
                    continue

            reaction_dict = {'Like': [], 'Love': [],
                             'Haha': [], 'Wow': [], 'Sad': [], 'Angry': []}

            reactions_box = driver.find_element(
                By.CSS_SELECTOR, 'div.rpm2j7zs.k7i0oixp.gvuykj2m.j83agx80.cbu4d94t.ni8dbmo4.du4w35lb.q5bimw55.ofs802cu.pohlnb88.dkue75c7.mb9wzai9.l56l04vs.r57mb794.l9j0dhe7.kh7kg01d.eg9m0zos.c3g1iek1.otl40fxz.cxgpxx05.rz4wbd8a.sj5x9vvc.a8nywdso')

            reactions = reactions_box.find_elements(
                By.CSS_SELECTOR, 'div.ow4ym5g4.auili1gw.rq0escxv.j83agx80.buofh1pr.g5gj957u.i1fnvgqd.oygrvhab.cxmmr5t8.hcukyx3x.kvgmc6g5.hpfvmrgz.qt6c0cv9.jb3vyjys.l9j0dhe7.du4w35lb.bp9cbjyn.btwxx1t3.dflh9lhu.scb9dxdr.nnctdnn4')

            # if reactions exist
            # loop through each reaction
            # find the emoji image of the reaction
            # add the user's name that made the reaction to the correct reaction section in the dictionary
            # return the reactions dictionary
            if len(reactions) > 0:

                for reaction in reactions:

                    emoji = reaction.find_element(
                        By.CSS_SELECTOR, 'img.hu5pjgll.bixrwtb6')

                    reaction_index = list(REACTIONS.values()).index(
                        emoji.get_attribute('src'))

                    reactor = reaction.find_element(
                        By.CSS_SELECTOR, 'a.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gpro0wi8.oo9gr5id.lrazzd5p').text

                    reaction_name = list(REACTIONS.keys())[reaction_index]

                    reaction_dict[reaction_name].append(reactor)

                exit_button = driver.find_element(
                    By.CSS_SELECTOR, 'div.oajrlxb2.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.nhd2j8a9.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.i1ao9s8h.esuyzwwr.f1sip0of.abiwlrkh.p8dawk7l.lzcic4wl.bp9cbjyn.s45kfl79.emlxlaya.bkmhp75w.spb7xbtv.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.j83agx80.taijpn5t.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.tv7at329.thwo4zme.tdjehn4e')

                driver.execute_script("arguments[0].click();", exit_button)

                time.sleep(random.randint(2, 5))

                return reaction_dict

            # otherwise, return None
            else:

                return None

        else:

            return None

    else:

        return None


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

    # if the post type is a comment
    # get the reactions of the comment
    elif post_type == 'comment':

        reactions = get_reactions(post, 'comment')

        # if reactions exist
        # count the reactions
        # return the count in string form
        if reactions != None:

            count = 0

            for reaction in reactions:

                results = reactions[reaction]

                count += len(results)

            return str(count)

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


def get_comment_ids(post_id: int, post: object) -> list:
    """Retrieves the list of comment ids for the ability to find the post comments

    Args:
        post (object): The WebElement object that represents a post or comment
        post_type (str): Either 'post' or 'comment', allows for correct element searching

    Returns:
        list: The provided post's comment ids
    """

    # get the number of comments of the post
    num_comments = get_num_comments(post)

    # if the number of comments does not equal None
    # turn the number into an integer
    if num_comments != None:

        num_comments = int(num_comments)

        # if the number of comments is bigger than 0
        # create and return the list of comment ids
        if num_comments > 0:

            return [str(post_id) + '_' + str(num) for num in range(1, num_comments + 1)]

        # otherwise, return None...
        else:

            return None

    else:

        return None


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


def get_comment_data(post: object, post_id: int, output_file: str):
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

        comment_id = 1

        for comment in comments:

            data = [{
                'post_id': str(post_id) + '_' + str(comment_id),
                'author': get_author(comment, 'comment'),
                'date': get_date(comment, 'comment'),
                'text': get_text(comment, 'comment'),
                'media': get_media(comment, 'comment'),
                'comment ids': None,
                'reactions': get_reactions(comment, 'comment'),
                '# comments': None,
                '# reactions': get_num_reactions(comment, 'comment'),
                '# shares': None
            }]

            upload_data(data, output_file)

            comment_id += 1


def get_page_data(page_ids: list, dates: list, limit: int, keywords: list, output_file: str):
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

    # loop through each page
    for page_id in page_ids:

        # loop through each keyword within each page
        for keyword in keywords:

            # loop through each date per keyword per page
            for date in dates:

                # go to the website with the correct page id, keyword, and date
                driver.get('https://www.facebook.com/page/' +
                           page_id + '/search?q=' + keyword + date)
                time.sleep(25)

                # scroll through the whole page and open all see more links
                scroll_page()
                open_see_more_links()

                # get every facebook post and loop through them
                posts = driver.find_elements(
                    By.CSS_SELECTOR, 'div.rq0escxv.l9j0dhe7.du4w35lb.hybvsw6c.io0zqebd.m5lcvass.fbipl8qg.nwvqtn77.k4urcfbm.ni8dbmo4.stjgntxs.sbcfpzgs')

                for post in posts:

                    # if the keyword is not in the post, skip it!
                    if keyword not in post.text.lower():

                        continue

                    # collect the data
                    data = [{
                        'post_id': post_id,
                        'author': get_author(post, 'post'),
                        'date': get_date(post, 'post'),
                        'text': get_text(post, 'post'),
                        'media': get_media(post, 'post'),
                        'comment ids': get_comment_ids(post_id, post),
                        'reactions': get_reactions(post, 'post'),
                        '# comments': get_num_comments(post),
                        '# reactions': get_num_reactions(post, 'post'),
                        '# shares': get_num_shares(post)
                    }]

                    # upload the data
                    upload_data(data, output_file)

                    # if there are comments
                    # get the comment data
                    if get_num_comments(post) != None:
                        get_comment_data(post, post_id, output_file)

                    # if there is a limit
                    # increment the limit since a new post was added
                    if limit != None:
                        limit_count += 1

                        # if the limit was hit
                        # let the user know and quit the program
                        if limit_count == limit:
                            print('Limit has been hit, all done!')
                            driver.quit()

                    # increment post id
                    post_id += 1


def get_group_data(group_ids: list, dates: list, limit: int, keywords: list, output_file: str):
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

    # initialize limit count and post id
    limit_count = 0
    post_id = 1

    # loop through every group
    for group_id in group_ids:

        # loop through every keyword within each group
        for keyword in keywords:

            # loop through every date per keyword per group
            for date in dates:

                # go to the correct website of the correct group id, keyword, and date
                driver.get('https://www.facebook.com/groups/' +
                           group_id + '/search?q=' + keyword + date)
                time.sleep(25)

                # scroll through the whole page and open all see more links
                scroll_page()
                open_see_more_links()

                # get every facebook post and loop through them
                posts = driver.find_elements(
                    By.CSS_SELECTOR, 'div.rq0escxv.l9j0dhe7.du4w35lb.hybvsw6c.io0zqebd.m5lcvass.fbipl8qg.nwvqtn77.k4urcfbm.ni8dbmo4.stjgntxs.sbcfpzgs')

                for post in posts:

                    # if the keyword is not in the post, skip the post
                    if keyword not in post.text.lower():

                        continue

                    # colelct the data
                    data = [{
                        'post_id': post_id,
                        'author': get_author(post, 'post'),
                        'date': get_date(post, 'post'),
                        'text': get_text(post, 'post'),
                        'media': get_media(post, 'post'),
                        'comment ids': get_comment_ids(post_id, post),
                        'reactions': get_reactions(post, 'post'),
                        '# comments': get_num_comments(post),
                        '# reactions': get_num_reactions(post, 'post'),
                        '# shares': get_num_shares(post)
                    }]

                    # upload the data
                    upload_data(data, output_file)

                    # if there are comments
                    # collect the comment data
                    if get_num_comments(post) != None:
                        get_comment_data(post, post_id, output_file)

                    # if there is a limit
                    # increment the limit count
                    if limit != None:
                        limit_count += 1

                        # if the limit count is hit
                        # let the user know and quit the program
                        if limit_count == limit:
                            print('Limit has been hit, all done!')
                            driver.quit()

                    # increment the post id
                    post_id += 1


def FacebookScraper(limit: int, start_year: str, username: str, password: str, group_ids: str, page_ids: str, keywords_file: str, output_file: str, chromedriver: str):
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

    # declare global variables
    global driver

    # configure the driver
    driver = configure_driver(chromedriver)

    # create the output file
    create_output_file(output_file)

    # create list of keywords
    keywords = get_keyword_list(keywords_file)

    # if a start year exists
    # create a list of date filters to run through
    if start_year != None:

        dates = get_dates_list(start_year)

    # otherwise, use the normal non-dated filter
    else:

        dates = [
            '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9In0%3D']

    # login to Facebook
    login(username, password)

    # if group ids exist
    # create a list
    # get the group data (posts and comments)
    if group_ids != None:

        group_ids = get_id_list(group_ids)
        get_group_data(group_ids, dates, limit, keywords, output_file)

    # if page ids exist
    # create a list
    # get the page data (posts and comments)
    if page_ids != None:

        page_ids = get_id_list(page_ids)
        get_page_data(page_ids, dates, limit, keywords, output_file)

    # let the user know the program is finished
    # quit the program
    print('All done!')
    driver.quit()


def main():

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
        help='List of Facebook Group IDS, ex: 12345678, 91011121314',
        type=str,
        default=None
    )

    parser.add_argument(
        '-pi',
        '--page_ids',
        help='List of Facebook Page IDS, ex: 12345678, 91011121314',
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

    FacebookScraper(
        args.limit,
        args.start_year,
        args.username,
        args.password,
        args.group_ids,
        args.page_ids,
        args.keywords_file,
        args.output_file,
        args.chromedriver
    )


if __name__ == '__main__':
    main()
