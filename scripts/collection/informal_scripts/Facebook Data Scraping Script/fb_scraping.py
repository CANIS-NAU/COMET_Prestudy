# import modules and libraries
from pydoc import classname
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, requests, random
from bs4 import BeautifulSoup as bs

# configuration stuff for Selenium
options = Options()
# this keeps track of cookies so login doesn't need to happen every time
options.add_argument("--user-data-dir=C:\\Users\\kylie\\Documents\\COMET Lab\\Facebook Data Scraping Script\\UserData")
options.page_load_strategy = 'normal'
# location of driver
driver = webdriver.Chrome(options=options, executable_path=r"C:\Users\kylie\Documents\COMET_Prestudy\scripts\collection\informal_scripts\Facebook Data Scraping Script\chromedriver.exe")


# array of group ids
group_ids = ['909093719101314', '1499960423615985', '265488540315007', '2200898567', '199119778025853']

# open keywords file
keywords = open('clean_keywords.txt', 'r')

##### start automation of facebook groups #####
database = []
post_id = 1
f = open('test.txt', 'w')

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
        for xpath in post_xpaths[2:]:

            # click on the post
            driver.find_element_by_xpath(xpath).click()
            time.sleep(random.randint(2, 5)) # wait for the post page to load

            # if i can change most recent to all comments, do so 
            if len(driver.find_elements(By.CLASS_NAME, '_2uak')) > 0:
                dropdown = driver.find_element(By.CLASS_NAME, '_2uak')
                dropdown.click()
                time.sleep(random.randint(1, 5))
                all_comments_option = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/select/option[2]')
                print(all_comments_option)
                all_comments_option.click()
                time.sleep(random.randint(2, 5))

            # find every reply in the post
            replies = driver.find_elements(By.CSS_SELECTOR, 'div._2b1h.async_elem')

            # open all replies on the post
            for reply in replies:
                reply.click()
                time.sleep(random.randint(2, 5))

            # get html with beautiful soup
            full_html = bs(driver.page_source, 'html.parser')

            # get main post details
            main_post = full_html.find('div', 'story_body_container')
            post_creator = main_post.find_all('a')[1].text
            post_group = main_post.find_all('a')[2].text
            post_date = main_post.find('abbr').text
            if post_date.split(' ')[2] < '2017':
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
                continue

            post_text = main_post.find('div', '_5rgt _5nk5').text
            post_text = post_text.encode("ascii", "ignore")
            post_text = post_text.decode()
            post_media = []
            post_mentions = []
            post_num_shares = 0
            post_num_reactions = 0
            post_num_like = 0
            post_num_love = 0
            post_num_care = 0
            post_num_haha = 0
            post_num_wow = 0
            post_num_sad = 0
            post_num_angry = 0
            reactions = []

            if full_html.find('div', '_43lx _55wr') != None:
                post_num_shares = int(full_html.find('div', '_43lx _55wr').find('span').text.split(' ')[0])

            if len(driver.find_elements(By.CSS_SELECTOR, 'div._1w1k._5c4t')) > 0:
                driver.find_element(By.CSS_SELECTOR, 'div._1w1k._5c4t').click()
                time.sleep(random.randint(1, 5))
                reactions_html = bs(driver.page_source, 'html.parser')
                for reaction in reactions_html.find_all('span', '_10tn'):
                    if reaction.find('span').parent['data-store'] != '{"reactionID":"all"}':
                        reactions.append(reaction.find('span')['aria-label'])

                print(reactions)
                time.sleep(0.5)
                driver.find_element(By.CLASS_NAME, '_6j_c').click()
                time.sleep(random.randint(1, 5))

            for reaction in reactions:
                print(reaction)
                post_num_reactions += int(reaction.split(' ')[0])
                if 'Like' in reaction:
                    post_num_like += int(reaction.split(' ')[0])
                elif 'Love' in reaction:
                    post_num_love += int(reaction.split(' ')[0])
                elif 'Care' in reaction:
                    post_num_care += int(reaction.split(' ')[0])
                elif 'Haha' in reaction:
                    post_num_haha += int(reaction.split(' ')[0])
                elif 'Wow' in reaction:
                    post_num_wow += int(reaction.split(' ')[0])
                elif 'Sad' in reaction:
                    post_num_sad += int(reaction.split(' ')[0])
                elif 'Angry' in reaction:
                    post_num_angry += int(reaction.split(' ')[0])

            database.append({'id': post_id, 'creator': post_creator, 'group': post_group, 'date': post_date, 'text': post_text, 'media': post_media, 'mentions': post_mentions, '# of shares': post_num_shares, '# of reactions': post_num_reactions, '# of like': post_num_like, '# of love': post_num_love, '# of care': post_num_care, '# of wow': post_num_wow, '# of haha': post_num_haha, '# of sad': post_num_sad, '# of angry': post_num_angry})

            # get comment and reply post details
            comments_replies = full_html.find_all('div', '_14v5')
            comment_reply_dates = full_html.find_all('abbr', '_4ghv _2b0a')
            comment_reply_id = 1

            for comment_reply in comments_replies:
                comment_reply_id_str = str(post_id) + '-' + str(comment_reply_id)
                comment_reply_creator = comment_reply.find('a').text
                comment_reply_date = comment_reply_dates[comments_replies.index(comment_reply)].text
                comment_reply_text = comment_reply.find('div', '_2b06').text.replace(comment_reply_creator, '')
                comment_reply_text = comment_reply_text.encode("ascii", "ignore")
                comment_reply_text = comment_reply_text.decode()
                comment_reply_media = []
                comment_reply_mentions = [mention.text for mention in comment_reply.find('div', '_2b06').find_all('a')[1:]]
                comment_reply_num_shares = 0
                comment_reply_num_reactions = 0
                comment_reply_num_like = 0
                comment_reply_num_love = 0
                comment_reply_num_care = 0
                comment_reply_num_haha = 0
                comment_reply_num_wow = 0
                comment_reply_num_sad = 0
                comment_reply_num_angry = 0
                reactions = []

                if len(driver.find_elements(By.CSS_SELECTOR, 'a._14v8._4edm')) > 0 and len(driver.find_elements(By.CSS_SELECTOR, 'a._14v8._4edm')) > comments_replies.index(comment_reply):
                    driver.find_elements(By.CSS_SELECTOR, 'a._14v8._4edm')[comments_replies.index(comment_reply)].click()
                    time.sleep(random.randint(2, 5))
                    reactions_html = bs(driver.page_source, 'html.parser')
                    for reaction in reactions_html.find_all('span', '_10tn'):
                        if reaction.find('span').parent['data-store'] != '{"reactionID":"all"}':
                            reactions.append(reaction.find('span')['aria-label'])
                    print(reactions)
                    time.sleep(0.5)
                    driver.find_element(By.CLASS_NAME, '_6j_c').click()

                for reaction in reactions:
                    print(reaction)
                    comment_reply_num_reactions += int(reaction.split(' ')[0])
                    if 'Like' in reaction:
                        comment_reply_num_like += int(reaction.split(' ')[0])
                    elif 'Love' in reaction:
                        comment_reply_num_love += int(reaction.split(' ')[0])
                    elif 'Care' in reaction:
                        comment_reply_num_care += int(reaction.split(' ')[0])
                    elif 'Haha' in reaction:
                        comment_reply_num_haha += int(reaction.split(' ')[0])
                    elif 'Wow' in reaction:
                        comment_reply_num_wow += int(reaction.split(' ')[0])
                    elif 'Sad' in reaction:
                        comment_reply_num_sad += int(reaction.split(' ')[0])
                    elif 'Angry' in reaction:
                        comment_reply_num_angry += int(reaction.split(' ')[0])

                database.append({'id': comment_reply_id_str, 'creator': comment_reply_creator, 'group': post_group, 'date': comment_reply_date, 'text': comment_reply_text, 'media': comment_reply_media, 'mentions': comment_reply_mentions, '# of shares': comment_reply_num_shares, '# of reactions': comment_reply_num_reactions, '# of like': comment_reply_num_like, '# of love': comment_reply_num_love, '# of care': comment_reply_num_care, '# of wow': comment_reply_num_wow, '# of haha': comment_reply_num_haha, '# of sad': comment_reply_num_sad, '# of angry': comment_reply_num_angry})

                comment_reply_id += 1

            post_id += 1
            for data in database:
                print(data)

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

f.close()