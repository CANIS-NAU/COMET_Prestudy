# import modules and libraries
from pydoc import classname
from jmespath import search
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, requests, random, pandas
from bs4 import BeautifulSoup as bs

def get_data(group_ids, keywords, filters):
    global post_id, data
    # loop through every group id
    for group in group_ids:

        # loop through every keyword
        for keyword in keywords:

            # loop through every filter for the keyword
            for filter in filters:

                # url of facebook group, keyword, and filter
                url = 'https://www.facebook.com/groups/' + group + '/search?q=' + keyword + filter
                
                # go to the url
                driver.get(url)

                scroll_down_page()

                open_all_comments()

                open_view_more_buttons()

                open_see_more_buttons()

                # get page html
                time.sleep(5)
                page_html = bs(driver.page_source, 'html.parser')

                # make sure the keyword is actually in the page text
                worthy = keyword.strip() in page_html.text.lower()
                # if it is not, go to the next filter
                if not worthy:
                    continue

                # get the page feed
                feed = page_html.find('div', 'd2edcug0 o7dlgrpb')
                # get the posts
                posts = feed.find_all('div', 'du4w35lb k4urcfbm l9j0dhe7 sjgh65i0')

                # loop through each post
                for post in posts:
                    # initialize all necessary variables
                    name, date, fb_group, text_content, shared_post_name, shared_post_date,shared_post_text_content = None,None,None,None,None,None,None
                    num_of_comments,num_of_shares,num_of_reactions,num_of_likes,num_of_love,num_of_cares,num_of_hahas,num_of_wows,num_of_sads,num_of_angrys = 0,0,0,0,0,0,0,0,0,0
                    media_content,mentions,who_commented,comment_ids, who_shared, who_reacted, who_liked, who_loved, who_cared, who_hahad, who_wowed, who_sadded, who_angried,shared_post_media_content, shared_post_mentions = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
                    shared_post = False

                    # make sure the keyword is in the post
                    worthy = keyword.strip() in post.text.lower()
                    # if not, move on to the next post
                    if not worthy:
                        continue

                    # get the creator name and date of the post 
                    top_content = post.find('div', 'll8tlv6m j83agx80 btwxx1t3 n851cfcs hv4rvrfc dati1w0a pybr56ya') # shows name and date
                    name = top_content.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p').text
                    date = post.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw')['aria-label']

                    # get the facebook group that the post belongs to
                    fb_group = page_html.find('span', 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh jq4qci2q a3bd9o3v b1v8xokw m9osqain').text.replace('in ', '')

                    # get the text content of the post
                    if post.find_all('div', attrs={'dir': 'auto'}) != None:
                        if post.find('div', 'hqeojc4l') != None:
                            shared_post = True
                            if post.find_all('div', attrs={'dir': 'auto'})[0] not in post.find('div', 'hqeojc4l'):
                                text_content = post.find_all('div', attrs={'dir': 'auto'})[0].text.encode('ascii', 'ignore').decode()
                                shared_post_text_content = post.find_all('div', attrs={'dir': 'auto'})[1].text.encode('ascii', 'ignore').decode()
                            else:
                                shared_post_text_content = post.find_all('div', attrs={'dir': 'auto'})[0].text.encode('ascii', 'ignore').decode()
                            shared_post_media_content = [image['src'] for image in post.find('div', 'hqeojc4l').find_all('img')]
                            shared_post_top_content = post.find('div', 'hqeojc4l').find('div', 'btwxx1t3 j83agx80 cwj9ozl2')
                            shared_post_name = shared_post_top_content.find('h4', 'gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl aahdfvyu hzawbc8m').text
                            date = shared_post_top_content.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw')['aria-label']
                        else:
                            text_content = post.find('div', attrs={'dir': 'auto'}).text.encode('ascii', 'ignore').decode()
                                

                    # get the media content out of the post
                    if post.find('img', 'i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm') != None:
                        media_content = [img['src'] for img in post.find_all('img', 'i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm', {'referrerpolicy': 'origin-when-cross-origin'})]

                    ##### RESERVED FOR MENTIONS #####
                    ##### RESERVED FOR MENTIONS #####

                    # get number of comments and shares
                    bottom_content = post.find_all('span', 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v b1v8xokw m9osqain')
                    for content in bottom_content:
                        if 'Comment' in content.text:
                            num_of_comments = int(content.text.split(' ')[0])
                            comment_ids = [str(post_id) + '-' + str(num + 1) for num in range(0,num_of_comments)]
                            who_commented = []
                            [who_commented.append(commentor.text) for commentor in post.find_all('span', 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn mdeji52x e9vueds3 j5wam9gi lrazzd5p oo9gr5id') if commentor.text not in who_commented]

                        elif 'Share' in content.text:
                            num_of_shares = int(content.text.split(' ')[0])

                    current_post = driver.find_elements(By.CSS_SELECTOR, 'div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0')[posts.index(post)]
                    share_button = None
                    post_bottom_content = current_post.find_elements(By.CSS_SELECTOR, 'div.bp9cbjyn.m9osqain.j83agx80.jq4qci2q.bkfpd7mw.a3bd9o3v.kvgmc6g5.wkznzc2l.oygrvhab.dhix69tm.jktsbyx5.rz4wbd8a.osnr6wyh.a8nywdso.s1tcr66n')
                    if len(post_bottom_content) > 0:
                        post_bottom_content = post_bottom_content[0]
                        if num_of_shares > 0 and num_of_comments > 0:
                            share_button = post_bottom_content.find_elements(By.CSS_SELECTOR, 'div.oajrlxb2.gs1a9yip.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.nhd2j8a9.mg4g778l.pfnyh3mw.p7hjln8o.tgvbjcpo.hpfvmrgz.esuyzwwr.f1sip0of.n00je7tq.arfg74bv.qs9ysxi8.k77z8yql.pq6dq46d.btwxx1t3.abiwlrkh.lzcic4wl.dwo3fsh8.g5ia77u1.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.gmql0nx0.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.du4w35lb.gpro0wi8')[1]
                        elif num_of_shares > 0:
                            share_button = post_bottom_content.find_elements(By.CSS_SELECTOR, 'div.oajrlxb2.gs1a9yip.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.nhd2j8a9.mg4g778l.pfnyh3mw.p7hjln8o.tgvbjcpo.hpfvmrgz.esuyzwwr.f1sip0of.n00je7tq.arfg74bv.qs9ysxi8.k77z8yql.pq6dq46d.btwxx1t3.abiwlrkh.lzcic4wl.dwo3fsh8.g5ia77u1.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.gmql0nx0.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.du4w35lb.gpro0wi8')[0]

                    if share_button != None:
                        driver.execute_script("arguments[0].click();", share_button)
                        time.sleep(random.randint(2, 5))
                        scroll_down_page()
                        time.sleep(random.randint(2, 5))
                        share_box = bs(driver.page_source, 'html.parser')
                        share_box = share_box.find('div', 'dati1w0a hv4rvrfc f0kvp8a6 j83agx80')
                        who_shared = [name.text for name in share_box.find_all('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p')]
                        close_button = driver.find_element(By.CSS_SELECTOR, 'div.oajrlxb2.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.nhd2j8a9.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.i1ao9s8h.esuyzwwr.f1sip0of.abiwlrkh.p8dawk7l.lzcic4wl.bp9cbjyn.s45kfl79.emlxlaya.bkmhp75w.spb7xbtv.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.j83agx80.taijpn5t.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.tv7at329.thwo4zme.tdjehn4e')
                        driver.execute_script("arguments[0].click();", close_button)
                        time.sleep(random.randint(2, 5))

                    # get number of reactions
                    if post.find('span', 'pcp91wgn') != None:
                        num_of_reactions = int(post.find('span', 'pcp91wgn').text)
                        # get all reaction info
                        reactions_button = driver.find_elements(By.CSS_SELECTOR, 'span.pcp91wgn')[posts.index(post)]
                        driver.execute_script("arguments[0].click();", reactions_button)
                        time.sleep(random.randint(2, 5))
                        reactions = bs(driver.page_source, 'html.parser')
                        reactions_box = reactions.find('div', {'aria-label': 'Reactions'})
                        who_reacted = [reactor.text for reactor in reactions_box.find_all('div', 'gs1a9yip ow4ym5g4 auili1gw rq0escxv j83agx80 cbu4d94t buofh1pr g5gj957u i1fnvgqd oygrvhab cxmmr5t8 hcukyx3x kvgmc6g5 tgvbjcpo hpfvmrgz rz4wbd8a a8nywdso l9j0dhe7 du4w35lb rj1gh0hx pybr56ya f10w8fjw')]

                        reaction_types = {'like': 'https://scontent.xx.fbcdn.net/m1/v/t6/An8TxrncfS4U_evP89c2GTGoBe2r0S9YacO1JWgXsSujyi44y6BPf9kkfnteC4B3wzEXsYS1dwFIG3UcC1c_CnQTTPxJ2zIXeAxTrhL8YV0Sp8quSZo.png?ccb=10-5&oh=00_AT-zy1HvN7UHIxj5zx_YlPJpgZTZxUJrwGo1tMzT515AQw&oe=62924856&_nc_sid=55e238', 'love': 'https://scontent.xx.fbcdn.net/m1/v/t6/An_gITNN0Ds6xnioTKduC3iqXXKmHcF0TaMvC1o32T--llsYDRmAjtiWFZ4R0stgYTwjHPojz-hShHPtB7jPz6xck8JN3Tg0UaA0OqYOiezH8xJvjrc.png?ccb=10-5&oh=00_AT_LtlarNjtxMJ4Im4DE5Bv7fDRcQLbLW4XpxdQo82QmEA&oe=6290A70A&_nc_sid=55e238', 'care': 'https://scontent.xx.fbcdn.net/m1/v/t6/An8UT5zh0xj_ZBy831gcqoVKvjjaBF8jCucOr8PgCD5KlFQ-JaR1IyJrRavwOoHyP9H3HYdxmOZlVV9lBf8OPE_JF-bfAxKj5e1dyPTlBzKMTNoY2YlKLWo.png?ccb=10-5&oh=00_AT-_xCJ2oxzj5k5cTdR_b1U3iz24uMbi1EPRzggc3Pwyyg&oe=62905757&_nc_sid=55e238', 'wow': 'https://scontent.xx.fbcdn.net/m1/v/t6/An9wqz15qSJBbtkJMsumo0WeMIE_6_MbAVHA1LdiH0PgQ82pe50V_Ey2f1YPiEO4lxTLUrsjaXWUC1bTJ3NKmC9FEw2jDlT2KFDmX_N13xBOjzFU8ws.png?ccb=10-5&oh=00_AT_eFw3Ipo57NP3G8gZrA2_0FuK8cjU-rql2mHpx6lj70Q&oe=62909EC2&_nc_sid=55e238', 'haha': 'https://scontent.xx.fbcdn.net/m1/v/t6/An-THWPVXq6iGcl9m0xpRXz841UFwm90bi1X84tlxOb8AG7h_2L7pTpESZnYZ-V90dtWcspSSm2WT0yqmOIxbs7Ms6rYoZGGCYDIVXAaSAA9l2YWfA.png?ccb=10-5&oh=00_AT_lxta5MkvK6Ji6vVE6CYLG4397ZuuYD-t6BSPxdvE-uA&oe=628FC629&_nc_sid=55e238', 'sad': 'https://scontent.xx.fbcdn.net/m1/v/t6/An8Y5LK0k-qkMes9nYNV5vHn0mALQUIvZXTKK-xekAdyqSbtBsDEcK0-FCVj5Mb7Ycj3xrItHd6q8iTSOi1VEki42ICqEi72j_mjN03-qgfUiGvWFfy1.png?ccb=10-5&oh=00_AT8TsG1NOq3Fyue_SSmSmd0ErV89DDQDSOnEdLoV0GpPVw&oe=629017E5&_nc_sid=55e238', 'angry': 'https://scontent.xx.fbcdn.net/m1/v/t6/An_p_GtpsNlMDEVWZr4AFkAPfy93yAtD7360WrRMu5gFpN7XbkK_meoLOk_IRtI6AwKbiv7I2VaOaEwXhFWrmpNNBG8nKmGs_rVlYdUOYpXf3bWw.png?ccb=10-5&oh=00_AT_bOesQlERUY4io3Mbuji3RaGCYiNSqsw-EIeA4zrdQZQ&oe=62905A4C&_nc_sid=55e238'}
                        reaction_people = reactions.find_all('div', 'ow4ym5g4 auili1gw rq0escxv j83agx80 buofh1pr g5gj957u i1fnvgqd oygrvhab cxmmr5t8 hcukyx3x kvgmc6g5 hpfvmrgz qt6c0cv9 jb3vyjys l9j0dhe7 du4w35lb bp9cbjyn btwxx1t3 dflh9lhu scb9dxdr nnctdnn4')

                        for person in reaction_people:
                            if person.find('img', {'src': reaction_types['like']}) != None:
                                num_of_likes += 1
                                who_liked.append(person.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p').text)
                            elif person.find('img', {'src': reaction_types['love']}) != None:
                                num_of_love += 1
                                who_loved.append(person.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p').text)
                            elif person.find('img', {'src': reaction_types['care']}) != None:
                                num_of_cares += 1
                                who_cared.append(person.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p').text)
                            elif person.find('img', {'src': reaction_types['wow']}) != None:
                                num_of_wows += 1
                                who_wowed.append(person.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p').text)
                            elif person.find('img', {'src': reaction_types['haha']}) != None:
                                num_of_hahas += 1
                                who_hahad.append(person.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p').text)
                            elif person.find('img', {'src': reaction_types['sad']}) != None:
                                num_of_sads += 1
                                who_sadded.append(person.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p').text)
                            elif person.find('img', {'src': reaction_types['angry']}) != None:
                                num_of_angrys += 1
                                who_angried.append(person.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p').text)

                        close_button = driver.find_element(By.CSS_SELECTOR, 'div.oajrlxb2.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.nhd2j8a9.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.i1ao9s8h.esuyzwwr.f1sip0of.abiwlrkh.p8dawk7l.lzcic4wl.bp9cbjyn.s45kfl79.emlxlaya.bkmhp75w.spb7xbtv.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.j83agx80.taijpn5t.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.tv7at329.thwo4zme.tdjehn4e')
                        driver.execute_script("arguments[0].click();", close_button)
                        time.sleep(random.randint(2, 5))

                    df = pandas.DataFrame([[post_id,name,date,fb_group,text_content, media_content, mentions, num_of_comments, who_commented, comment_ids, num_of_shares, who_shared, num_of_reactions, who_reacted, num_of_likes, who_liked, num_of_love, who_loved, num_of_cares, who_cared, num_of_wows, who_wowed, num_of_hahas, who_hahad, num_of_sads, who_sadded, num_of_angrys, who_angried, shared_post, shared_post_name, shared_post_date, shared_post_text_content, shared_post_media_content]])
                    df.to_csv('facebook_tab.csv', mode='a', sep ='\t', header=False)
                    df.to_csv('facebook_comma.csv', mode = 'a', header=False)
                    
                    comments = post.find_all('div', 'rj1gh0hx buofh1pr ni8dbmo4 stjgntxs hv4rvrfc')
                    comment_id_num = 1
                    for comment in comments:
                        comment_id = str(post_id) + '-' + str(comment_id_num)
                        name, date, text_content, shared_post_name, shared_post_date,shared_post_text_content = None,None,None,None,None,None
                        num_of_comments,num_of_shares,num_of_reactions,num_of_likes,num_of_love,num_of_cares,num_of_hahas,num_of_wows,num_of_sads,num_of_angrys = 0,0,0,0,0,0,0,0,0,0
                        media_content,mentions,who_commented,comment_ids, who_shared, who_reacted, who_liked, who_loved, who_cared, who_hahad, who_wowed, who_sadded, who_angried,shared_post_media_content, shared_post_mentions = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
                        shared_post = False

                        name = comment.find('span', 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn mdeji52x e9vueds3 j5wam9gi lrazzd5p oo9gr5id').text
                        date = comment.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 m9osqain knj5qynh').text
                        text_content = comment.find('div', 'ecm0bbzt e5nlhep0 a8c37x1j').text
                        if comment.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p') != None:
                            mentions = [name.text for name in comment.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p')]
                        media_content = [image['src'] for image in comment.find_all('img') if 'data:image' not in image['src'] ]

                        # get number of reactions
                        if comment.find('div', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of n00je7tq arfg74bv qs9ysxi8 k77z8yql l9j0dhe7 abiwlrkh p8dawk7l lzcic4wl') != None:
                            num_of_reactions = int(comment.find('div', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of n00je7tq arfg74bv qs9ysxi8 k77z8yql l9j0dhe7 abiwlrkh p8dawk7l lzcic4wl')['aria-label'].split(' ')[0])
                            # get all reaction info
                            driver_post = driver.find_elements(By.CSS_SELECTOR, 'div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0')[posts.index(post)]
                            driver_comment = driver_post.find_elements(By.CSS_SELECTOR, 'div.rj1gh0hx.buofh1pr.ni8dbmo4.stjgntxs.hv4rvrfc')[comments.index(comment)]
                            reactions_button = driver_comment.find_elements(By.CSS_SELECTOR, 'div.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.n00je7tq.arfg74bv.qs9ysxi8.k77z8yql.l9j0dhe7.abiwlrkh.p8dawk7l.lzcic4wl')[0]
                            driver.execute_script("arguments[0].click();", reactions_button)
                            time.sleep(random.randint(2, 5))
                            reactions = bs(driver.page_source, 'html.parser')
                            reactions_box = reactions.find('div', {'aria-label': 'Reactions'})
                            who_reacted = [reactor.text for reactor in reactions_box.find_all('div', 'gs1a9yip ow4ym5g4 auili1gw rq0escxv j83agx80 cbu4d94t buofh1pr g5gj957u i1fnvgqd oygrvhab cxmmr5t8 hcukyx3x kvgmc6g5 tgvbjcpo hpfvmrgz rz4wbd8a a8nywdso l9j0dhe7 du4w35lb rj1gh0hx pybr56ya f10w8fjw')]

                            reaction_types = {'like': 'https://scontent.xx.fbcdn.net/m1/v/t6/An8TxrncfS4U_evP89c2GTGoBe2r0S9YacO1JWgXsSujyi44y6BPf9kkfnteC4B3wzEXsYS1dwFIG3UcC1c_CnQTTPxJ2zIXeAxTrhL8YV0Sp8quSZo.png?ccb=10-5&oh=00_AT-zy1HvN7UHIxj5zx_YlPJpgZTZxUJrwGo1tMzT515AQw&oe=62924856&_nc_sid=55e238', 'love': 'https://scontent.xx.fbcdn.net/m1/v/t6/An_gITNN0Ds6xnioTKduC3iqXXKmHcF0TaMvC1o32T--llsYDRmAjtiWFZ4R0stgYTwjHPojz-hShHPtB7jPz6xck8JN3Tg0UaA0OqYOiezH8xJvjrc.png?ccb=10-5&oh=00_AT-sXLkhu-lJ6fKVktjxnCO6cMoirjzYKKGsfVZDbSUg7g&oe=6292A14A&_nc_sid=55e238', 'care': 'https://scontent.xx.fbcdn.net/m1/v/t6/An8UT5zh0xj_ZBy831gcqoVKvjjaBF8jCucOr8PgCD5KlFQ-JaR1IyJrRavwOoHyP9H3HYdxmOZlVV9lBf8OPE_JF-bfAxKj5e1dyPTlBzKMTNoY2YlKLWo.png?ccb=10-5&oh=00_AT-_xCJ2oxzj5k5cTdR_b1U3iz24uMbi1EPRzggc3Pwyyg&oe=62905757&_nc_sid=55e238', 'wow': 'https://scontent.xx.fbcdn.net/m1/v/t6/An9wqz15qSJBbtkJMsumo0WeMIE_6_MbAVHA1LdiH0PgQ82pe50V_Ey2f1YPiEO4lxTLUrsjaXWUC1bTJ3NKmC9FEw2jDlT2KFDmX_N13xBOjzFU8ws.png?ccb=10-5&oh=00_AT8zzQF_DIeM4zPM08Rbcfbg3o7uDwZNZodlAECcPjEtdQ&oe=62929902&_nc_sid=55e238', 'haha': 'https://scontent.xx.fbcdn.net/m1/v/t6/An-THWPVXq6iGcl9m0xpRXz841UFwm90bi1X84tlxOb8AG7h_2L7pTpESZnYZ-V90dtWcspSSm2WT0yqmOIxbs7Ms6rYoZGGCYDIVXAaSAA9l2YWfA.png?ccb=10-5&oh=00_AT8jHvlHQ-diiLrL2C4ahw79DswfJ5H7-ZcsNAEWnVkOJA&oe=6291C069&_nc_sid=55e238', 'sad': 'https://scontent.xx.fbcdn.net/m1/v/t6/An8Y5LK0k-qkMes9nYNV5vHn0mALQUIvZXTKK-xekAdyqSbtBsDEcK0-FCVj5Mb7Ycj3xrItHd6q8iTSOi1VEki42ICqEi72j_mjN03-qgfUiGvWFfy1.png?ccb=10-5&oh=00_AT_e6V47_acgYerbr976K6eTTJc66jqTy3HQngnRk1JOJg&oe=62921225&_nc_sid=55e238', 'angry': 'https://scontent.xx.fbcdn.net/m1/v/t6/An8ph2gwH6WsvW6pxuYzGzrW8CdpQXACl5PKb5e3I8yS82dPyO-cHlpZDGDHuNFUBIPS8_rJmr6L5JKI6gpOd6GVgh3sLHS6qMD_fv-qg6FoJAzZC2k.png?ccb=10-5&oh=00_AT97ntOkWfs4h5ch2bjfKDtETDJaTMRu_62Nm5YMyltb5g&oe=6292ADCC&_nc_sid=55e238'}
                            reaction_people = reactions.find_all('div', 'ow4ym5g4 auili1gw rq0escxv j83agx80 buofh1pr g5gj957u i1fnvgqd oygrvhab cxmmr5t8 hcukyx3x kvgmc6g5 hpfvmrgz qt6c0cv9 jb3vyjys l9j0dhe7 du4w35lb bp9cbjyn btwxx1t3 dflh9lhu scb9dxdr nnctdnn4')

                            for person in reaction_people:
                                if person.find('img', {'src': reaction_types['like']}) != None:
                                    num_of_likes += 1
                                    who_liked.append(person.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p').text)
                                elif person.find('img', {'src': reaction_types['love']}) != None:
                                    num_of_love += 1
                                    who_loved.append(person.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p').text)
                                elif person.find('img', {'src': reaction_types['care']}) != None:
                                    num_of_cares += 1
                                    who_cared.append(person.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p').text)
                                elif person.find('img', {'src': reaction_types['wow']}) != None:
                                    num_of_wows += 1
                                    who_wowed.append(person.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p').text)
                                elif person.find('img', {'src': reaction_types['haha']}) != None:
                                    num_of_hahas += 1
                                    who_hahad.append(person.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p').text)
                                elif person.find('img', {'src': reaction_types['sad']}) != None:
                                    num_of_sads += 1
                                    who_sadded.append(person.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p').text)
                                elif person.find('img', {'src': reaction_types['angry']}) != None:
                                    num_of_angrys += 1
                                    who_angried.append(person.find('a', 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p').text)

                            close_button = driver.find_element(By.CSS_SELECTOR, 'div.oajrlxb2.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.nhd2j8a9.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.i1ao9s8h.esuyzwwr.f1sip0of.abiwlrkh.p8dawk7l.lzcic4wl.bp9cbjyn.s45kfl79.emlxlaya.bkmhp75w.spb7xbtv.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.j83agx80.taijpn5t.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.tv7at329.thwo4zme.tdjehn4e')
                            driver.execute_script("arguments[0].click();", close_button)
                            time.sleep(random.randint(2, 5))            

                        df = pandas.DataFrame([[comment_id,name,date,fb_group,text_content, media_content, mentions, num_of_comments, who_commented, comment_ids, num_of_shares, who_shared, num_of_reactions, who_reacted, num_of_likes, who_liked, num_of_love, who_loved, num_of_cares, who_cared, num_of_wows, who_wowed, num_of_hahas, who_hahad, num_of_sads, who_sadded, num_of_angrys, who_angried, shared_post, shared_post_name, shared_post_date, shared_post_text_content, shared_post_media_content]])
                        df.to_csv('facebook_tab.csv', mode='a', sep ='\t', header=False)
                        df.to_csv('facebook_comma.csv', mode = 'a', header=False)
                        comment_id_num += 1

                    post_id += 1

def open_all_comments():
    possible_comment_buttons = driver.find_elements(By.CSS_SELECTOR, 'div.oajrlxb2.gs1a9yip.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.nhd2j8a9.mg4g778l.pfnyh3mw.p7hjln8o.tgvbjcpo.hpfvmrgz.esuyzwwr.f1sip0of.n00je7tq.arfg74bv.qs9ysxi8.k77z8yql.pq6dq46d.btwxx1t3.abiwlrkh.lzcic4wl.dwo3fsh8.g5ia77u1.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.gmql0nx0.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.du4w35lb.gpro0wi8')

    for possible_comment_button in possible_comment_buttons:
        if 'Comment' in str(possible_comment_button.get_attribute('innerHTML')):
            driver.execute_script("arguments[0].click();", possible_comment_button)
            time.sleep(random.randint(2, 5))

def scroll_down_page():
    last_height = driver.execute_script('return document.body.scrollHeight')

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height

def open_see_more_buttons():
    while True:
        see_more_count = 0
        possible_see_more_buttons = driver.find_elements(By.CSS_SELECTOR, 'div.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gpro0wi8.oo9gr5id.lrazzd5p')

        for possible_see_more_button in possible_see_more_buttons:
            if 'See more' in str(possible_see_more_button.get_attribute('innerHTML')):
                see_more_count += 1
                driver.execute_script("arguments[0].click();", possible_see_more_button)
                time.sleep(random.randint(2, 5))

        if see_more_count == 0:
            break

def open_view_more_buttons():
    while True:
        view_count = 0
        possible_view_more_comments_buttons = driver.find_elements(By.CSS_SELECTOR, 'div.oajrlxb2.g5ia77u1.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.nhd2j8a9.mg4g778l.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.tgvbjcpo.hpfvmrgz.jb3vyjys.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.esuyzwwr.f1sip0of.du4w35lb.n00je7tq.arfg74bv.qs9ysxi8.k77z8yql.pq6dq46d.btwxx1t3.abiwlrkh.lzcic4wl.bp9cbjyn.m9osqain.buofh1pr.g5gj957u.p8fzw8mz.gpro0wi8')

        for possible_view_more_comments_button in possible_view_more_comments_buttons:
            if 'View' in str(possible_view_more_comments_button.get_attribute('innerHTML')) or 'Replies' in str(possible_view_more_comments_button.get_attribute('innerHTML')):
                view_count += 1
                driver.execute_script("arguments[0].click();", possible_view_more_comments_button)
                time.sleep(random.randint(2, 5))

        if view_count == 0:
            break

# configuration stuff for Selenium
options = Options()
# this keeps track of cookies so login doesn't need to happen every time
options.add_argument("--user-data-dir=C:\\Users\\kylie\\Documents\\COMET Lab\\Facebook Data Scraping Script\\UserData")
options.page_load_strategy = 'normal'
# location of driver
driver = webdriver.Chrome(options=options, executable_path=r"C:\Users\kylie\Documents\COMET_Prestudy\scripts\collection\informal_scripts\Facebook Data Scraping Script\chromedriver.exe")


# array of group ids
group_ids = ['909093719101314', '1499960423615985', '265488540315007', '2200898567', '199119778025853']

# array of filters: 2017, 2018, 2019, 2020, 2021, 2022
filters = ['&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAxN1xcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAxNy0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDE3XFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAxNy0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMTctMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMTctMTItMzFcXFwifVwifSJ9', '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAxOFxcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAxOC0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDE4XFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAxOC0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMTgtMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMTgtMTItMzFcXFwifVwifSJ9', '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAxOVxcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAxOS0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDE5XFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAxOS0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMTktMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMTktMTItMzFcXFwifVwifSJ9', '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAyMFxcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAyMC0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDIwXFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAyMC0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMjAtMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMjAtMTItMzFcXFwifVwifSJ9', '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAyMVxcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAyMS0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDIxXFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAyMS0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMjEtMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMjEtMTItMzFcXFwifVwifSJ9', '&filters=eyJycF9jaHJvbm9fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9IiwicnBfY3JlYXRpb25fdGltZTowIjoie1wibmFtZVwiOlwiY3JlYXRpb25fdGltZVwiLFwiYXJnc1wiOlwie1xcXCJzdGFydF95ZWFyXFxcIjpcXFwiMjAyMlxcXCIsXFxcInN0YXJ0X21vbnRoXFxcIjpcXFwiMjAyMi0xXFxcIixcXFwiZW5kX3llYXJcXFwiOlxcXCIyMDIyXFxcIixcXFwiZW5kX21vbnRoXFxcIjpcXFwiMjAyMi0xMlxcXCIsXFxcInN0YXJ0X2RheVxcXCI6XFxcIjIwMjItMS0xXFxcIixcXFwiZW5kX2RheVxcXCI6XFxcIjIwMjItMTItMzFcXFwifVwifSJ9']

# open keywords file
keywords = open('clean_keywords.txt', 'r')

########## start automation of facebook groups ##########
post_id = 1 # tracks post ids
df = pandas.DataFrame(columns=['id','name','date','fb_group','text_content', 'media_content', 'mentions', 'num_of_comments', 'who_commented', 'comment_ids', 'num_of_shares', 'who_shared', 'num_of_reactions', 'who_reacted', 'num_of_likes', 'who_liked', 'num_of_love', 'who_loved', 'num_of_cares', 'who_cared', 'num_of_wows', 'who_wowed', 'num_of_hahas', 'who_hahad', 'num_of_sads', 'who_sadded', 'num_of_angrys', 'who_angried', 'shared_post', 'shared_post_name', 'shared_post_date', 'shared_post_text_content', 'shared_post_media_content'])
df.to_csv('facebook_tab.csv', sep ='\t')
df.to_csv('facebook_comma.csv')
get_data(group_ids, keywords, filters)