from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import re
import pyautogui
import time
import pandas as pd
import random
import os
import shutil
import urllib.request
import pyperclip


search_query = 'tekken'



counter = 0

if not os.path.exists("backup"):
    os.mkdir("backup")

backup_path = os.path.join(os.getcwd(), "backup")
copy_path = os.path.join(os.getcwd(), "facebook.csv")


time_between_pagemove = 0.2
SCROLL_PAUSE_TIME = 5

option = Options()

option.add_argument("--disable-infobars")
# option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1
})

driver = webdriver.Chrome(chrome_options=option,
                          executable_path='C:\Windows\chromedriver.exe')
driver.get("https://facebook.com")

# Wait for facebook page to load
time.sleep(2)

pyautogui.keyDown('winleft')
pyautogui.press('up')
pyautogui.keyUp('winleft')

# Search the page in search bar
pyautogui.hotkey('ctrl', 'l')
time.sleep(1)
pyautogui.write('https://facebook.com/' + search_query + '/posts')
pyautogui.press('enter')

# # Get to the posts tab            -               Handled in above step
# posts_link = driver.find_element_by_xpath('''//span[contains(text(),'Posts')]''')
# posts_link.click()

time.sleep(6)

# Bypass not now
pyautogui.press('pagedown')
time.sleep(6)
pyautogui.press('pagedown')
time.sleep(5)
pyautogui.press('pagedown')
time.sleep(2)

try:
    not_now = driver.find_element_by_xpath(
        '''//a[@id='expanding_cta_close_button']''')
    not_now.click()
    time.sleep(2)
except:
    pass

if not os.path.exists('''D:\\1Touch\\facebook_images\\videos'''):
    os.mkdir('''D:\\1Touch\\facebook_images\\videos''')

print('The first step')
# Get the posts
while(True):

    time.sleep(7)


    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    # if new_height == last_height:
    #     break
    last_height = new_height



    post_class = driver.find_elements_by_css_selector('._4-u2._4-u8')
    posts_dataframe_list = []
    prevent_duplicate = 0

    image_name = 1

    for i in post_class[counter:]:
        prevent_duplicate += 1
        if(prevent_duplicate % 2 == 0):
            posts_dataframe_dict = dict()




            image_counter = 1

            #########################################################
            ############# Downloading post images ###################
            #########################################################
            for j in i.find_elements_by_css_selector('._3x-2'):
                # print(j)
                
                for k in j.find_elements_by_tag_name('img'):
                    image_post = k.get_attribute('src')
                    name_image = '''D:\\1Touch\\facebook_images\\''' + str(image_name) + "_" + str(image_counter) + '.jpg'
                    urllib.request.urlretrieve(image_post, name_image)
                    image_counter += 1

                for k in j.find_elements_by_tag_name('video'):

                    
                    name_video = '''D:\\1Touch\\facebook_images\\videos\\''' + str(image_name) + "_" + str(image_counter)
                    hover = ActionChains(driver).move_to_element(k)
                    hover.perform()              

                    time.sleep(1)
                    pyautogui.press('down')
                    time.sleep(.2)
                    pyautogui.press('down')
                    time.sleep(.1)
                    pyautogui.press('down')
                    time.sleep(.15)
                    pyautogui.press('down')
                    time.sleep(.12)
                    pyautogui.press('down')
                    time.sleep(.17)
                    pyautogui.press('down')

                    time.sleep(1)

                    hover1 = ActionChains(driver).move_to_element(k)
                    hover1.perform()  

                # Click the three dot menu under video
                for k in i.find_elements_by_css_selector('._zbd._42ft'):
                    for l in k.find_elements_by_tag_name('img'):
                        ActionChains(driver).move_to_element(l).click().perform()

                # Get the copy link object
                for k in i.find_elements_by_css_selector('._2iw7._2iw8'):
                    for l in k.find_elements_by_css_selector('._8s62._2iw4'):
                        video_link = ActionChains(driver).move_to_element(l).click().perform()

                posts_dataframe_dict['video_url'] = pyperclip.paste()
                image_counter += 1

                
            image_name += 1
            time.sleep(1)
            #########################################################
            ## Expand the view more comments object using selenium ##
            #########################################################
            for j in i.find_elements_by_css_selector("._7a94._7a9d"):
                for k in j.find_elements_by_tag_name('a'):
                    more_comments = ActionChains(driver).move_to_element(k)
                    more_comments.perform()
                    pyautogui.press('pagedown')
                    time.sleep(.2)
                    more_comments.click().perform()
                    time.sleep(5)

            ########################################################
            ############### Get the comments #####################
            ########################################################
            comments_posts = []
            for j in i.find_elements_by_tag_name('ul'):
                for k in j.find_elements_by_tag_name('li'):
                    soup_source = BeautifulSoup(k.get_attribute('innerHTML'), 'html.parser')
                    for l in soup_source.find_all('span', {"class":"_3l3x"}):
                        comments_posts.append(l.text)
            posts_dataframe_dict['comments'] = comments_posts


            ########################################################
            ########### Get the source html of each post ###########
            ########################################################
            x = BeautifulSoup(i.get_attribute('innerHTML'), 'html.parser')
            # print(x)
            # WORKING CODE BELOW           REACTIONS , COMMENTS , SHARES
            ################# Getting the title of post #####################
       


            for i in x.find_all('p'):
                try:
                    # print(i.text)
                    posts_dataframe_dict['title'] = i.text
                except:
                    pass
                break
            ################# Getting timestamp of the post ##################
            for i in x.find_all('span', {"class": {"timestampContent"}}):
                try:
                    # print(i.text)
                    posts_dataframe_dict['timestamp'] = i.text
                except:
                    pass

            ################## Getting the total reactions from a post ##################
            count = 0
            for i in x.find_all('span', {"class": "_1n9k"}):
                for j in i.find_all('a'):
                    # print(j['aria-label'])
                    if count == 2:
                        posts_dataframe_dict['care'] = j['aria-label']
                    if count == 1:
                        posts_dataframe_dict['love'] = j['aria-label']
                        count += 1
                    if count == 0:
                        posts_dataframe_dict['likes'] = j['aria-label']
                        count += 1
            for i in x.find_all('form'):

                ################## Getting the total reactions from a post ##################
                for j in i.find_all('a'):
                    for k in j.find_all('span', {"class": "_81hb"}):
                        # print(j)
                        try:
                            # print(j.text.strip()[-8:].strip())
                            # print(k.text)
                            posts_dataframe_dict['total_reactions'] = k.text
                        except:
                            pass
                        break
                ################### Getting the number of comments ###################
                for j in i.find_all('a', {"class": "_3hg- _42ft"}):
                    # Will get the commnets upto 3 digits ( limit : 999k)
                    posts_dataframe_dict['commnets'] = j.text
                    # print(j.text)
                    # print(j.text.strip()[0:3].strip())

                ################### Getting number of shares #####################
                for j in i.find_all('a', {"class": "_3rwx _42ft"}):
                    # Will get the shares upto 3 digits ( limit : 999k)
                    posts_dataframe_dict['total_reactions'] = j.text

            posts_dataframe_list.append(posts_dataframe_dict)

        counter = len(posts_dataframe_list)

        posts_dataframe = pd.DataFrame(posts_dataframe_list)
        posts_dataframe.to_csv(os.path.join(os.getcwd(), "facebook.csv"))
                
        pyperclip.copy('')

        print('Moving the file to backup')
        print(copy_path + " - > " + backup_path)
        shutil.copy2(copy_path, backup_path)

    time.sleep(10)
