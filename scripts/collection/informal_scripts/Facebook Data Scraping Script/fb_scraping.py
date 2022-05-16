# import modules and libraries
from pydoc import classname
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, requests
from bs4 import BeautifulSoup as bs

# configuration stuff for Selenium
options = Options()
# this keeps track of cookies so login doesn't need to happen every time
options.add_argument("--user-data-dir=C:\\Users\\kylie\\Documents\\COMET Lab\\Facebook Data Scraping Script\\UserData")
options.page_load_strategy = 'normal'
# location of driver
driver = webdriver.Chrome(options=options, executable_path=r"C:\Users\kylie\Documents\COMET Lab\Facebook Data Scraping Script\chromedriver.exe")

# array of group ids
group_ids = ['909093719101314', '1499960423615985', '265488540315007', '2200898567', '199119778025853']

# open keywords file
keywords = open('clean_keywords.txt', 'r')

##### start automation of facebook groups #####
database = []
post_id = 1

# loop through every group id
for group in group_ids:

    # 
    for keyword in keywords:

        url = 'https://m.facebook.com/groups/search/?groupID=' + group + '&query=internet&ref=content_filter&tsid=0.9675975027221222&source=typeahead'
        # search for keyword and filter in group
        driver.get(url)

        # scroll to the bottom of the page
        last_height = driver.execute_script('return document.body.scrollHeight')

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            new_height = driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break
            last_height = new_height

        # get the xpath of all posts
        post_xpaths = []
        count = 1
        post_type = 'beginning'
        xpath = '/html/body/div[1]/div/div[4]/div/div[1]/div/div[1]/div[' + str(count) + ']/div/div/div/div/div/div/div/div/div/div[3]'

        # loop through possible xpath of posts and append them to a list for access
        while True:
            if len(driver.find_elements(By.XPATH, xpath)) > 0:
                post_xpaths.append(xpath)
                count += 1

                if post_type == 'beginning':
                    xpath = '/html/body/div[1]/div/div[4]/div/div[1]/div/div[1]/div[' + str(count) + ']/div/div/div/div/div/div/div/div/div/div[3]'
                elif post_type == 'middle':
                    xpath  = '/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[1]/div/div/div/div[' + str(count) + ']/div/div/div/div/div/div/div[3]'
                elif post_type == 'ending':
                    xpath = '/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div/div[' + str(count) + ']/div/div/div/div/div/div/div[3]'
            else:
                count = 1
                if post_type == 'beginning':
                    post_type = 'middle'
                    xpath  = '/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[1]/div/div/div/div[' + str(count) + ']/div/div/div/div/div/div/div[3]'
                elif post_type == 'middle':
                    post_type = 'ending'
                    xpath = '/html/body/div[1]/div/div[4]/div/div[1]/div/div[2]/div[2]/div[1]/div/div/div/div[' + str(count) + ']/div/div/div/div/div/div/div[3]'
                else:
                    break

        # click on every post to collect data
        for xpath in post_xpaths:

            # click on the post
            driver.find_element_by_xpath(xpath).click()
            time.sleep(2) # wait for the post page to load

            # if i can change most recent to all comments, do so 
            if len(driver.find_elements(By.CLASS_NAME, '_2uak')) > 0:
                dropdown = driver.find_element(By.CLASS_NAME, '_2uak')
                dropdown.click()
                time.sleep(0.5)
                all_comments_option = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/select/option[2]')
                print(all_comments_option)
                all_comments_option.click()
                time.sleep(1)

            # find every reply in the post
            replies = driver.find_elements(By.CSS_SELECTOR, 'div._2b1h.async_elem')

            # open all replies on the post
            for reply in replies:
                reply.click()

            # get html with beautiful soup
            time.sleep(1)
            full_html = bs(driver.page_source, 'html.parser')

            # get main post details
            main_post = full_html.find('div', 'story_body_container')
            post_creator = main_post.find_all('a')[1].text
            post_group = main_post.find_all('a')[2].text
            post_date = main_post.find('abbr').text
            post_text = main_post.find('p').text
            post_shares = full_html.find('div', '_43lx _55wr').find('span').text 

            # get comment and reply post details
            comments_replies = full_html.find_all('div', '_14v5')
            comment_reply_dates = full_html.find_all('abbr', '_4ghv _2b0a')

            for comment_reply in comments_replies:
                comment_reply_creator = comment_reply.find('a').text
                comment_reply_date = comment_reply_dates[comments_replies.index(comment_reply)+1].text
                comment_reply_text = comment_reply.find('div', '_2b06').find_all('div')[1].text
                print(comment_reply_text)

            break

            driver.get(url)
            time.sleep(5)
            # scroll to the bottom of the page
            last_height = driver.execute_script('return document.body.scrollHeight')

            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)
                new_height = driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height:
                    break
                last_height = new_height
            
            time.sleep(2)

        time.sleep(90000)

        break
    break