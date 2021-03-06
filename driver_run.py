from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from collections import OrderedDict
import pandas as pd
import time
import pyautogui
import random
import os
import urllib.request
from tqdm import tqdm
import lxml

search = "PlayStation"


post_counter = 0

if not os.path.exists(os.path.join(search, 'images')):
    os.makedirs(os.path.join(search, 'images'))

# Global variables
post_class_css_selector = "._5pcr.userContentWrapper"
comment_class_css_selector = "._7a94._7a9d"
bypass_class = "._ohf.rfloat"
get_title_div_dict = {"data-testid":"post_message"}
get_timestamp_span_dict = {"class": "_5ptz"}
get_reactions_span_dict = {"class": "_1n9k"}
get_comments_span_dict = {"class": "_3l3x"}
get_num_share_anchor_dict = {"class": "_3rwx _42ft"}
get_images_div_css_selector = ".uiScaledImageContainer"

posts_dataframe_dict = OrderedDict()
posts_dataframe_list = []
posts_dataframe_capture = []

def no_login():
    for i in range(1,3):
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep((i+1)/2)

    not_now = driver.find_element_by_xpath(
        '''//a[@id='expanding_cta_close_button']''')
    not_now.click()
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(random.randint(2,4))

def selenium_source_posts():
    post_class = driver.find_elements_by_css_selector(post_class_css_selector)
    return post_class

def bypass():
    try:
        bypass_elem = driver.find_element_by_css_selector(bypass_class)
        for i in bypass_elem.find_elements_by_tag_name('a'):
            i.click()
            return
    except:
        pass

def beautiful_source_posts(post_class):
    x = []
    for i in post_class:
        x.append(BeautifulSoup(i.get_attribute('innerHTML'), 'html.parser'))
    
    return x

def get_title(i):
    for j in i.find_all('div', get_title_div_dict):
        text = ""
        for k in j.find_all('p'):
            if len(text) == 0:
                text = k.text
            else:
                text = " ".join([text, k.text])
        posts_dataframe_dict["title"] = text

def get_timestamp(i):
    for j in i.find_all('abbr', get_timestamp_span_dict):
        posts_dataframe_dict["timestamp"] = j['title']

def get_reactions(i):
    for j in i.find_all('span', get_reactions_span_dict):
        for k in j.find_all('a'):
            if k['aria-label'].lower().find('care') != -1:
                posts_dataframe_dict['care'] = k['aria-label']
            if k['aria-label'].lower().find('love') != -1:
                posts_dataframe_dict['love'] = k['aria-label']
            if k['aria-label'].lower().find('like') != -1:
                posts_dataframe_dict['likes'] = k['aria-label']
            if k['aria-label'].lower().find('wow') != -1:
                posts_dataframe_dict['wow'] = k['aria-label']
            if k['aria-label'].lower().find('haha') != -1:
                posts_dataframe_dict['haha'] = k['aria-label']
            if k['aria-label'].lower().find('sad') != -1:
                posts_dataframe_dict['sad'] = k['aria-label']

def get_num_shares(i):
    for j in i.find_all('a', get_num_share_anchor_dict):
        posts_dataframe_dict['shares'] = j.text

def extend_comments(i):
    for j in i.find_elements_by_css_selector(comment_class_css_selector):
        for k in j.find_elements_by_tag_name('a'):
            try:
                more_comments = ActionChains(driver).move_to_element(k)
                more_comments.perform()
                time.sleep(random.randint(1,2))
                pyautogui.press('pagedown')
                # more_comments.send_keys(Keys.PAGE_DOWN)
                time.sleep(random.randint(1,2))
                more_comments.click().perform()
                time.sleep(random.randint(3,6))
            except:
                pass

def get_comments(i):
    comments_posts = []

    try:
        for j in i.find_all('span', get_comments_span_dict):
            comments_posts.append(j.text)
        posts_dataframe_dict['comments'] = comments_posts
    except:
        pass

def get_images(i):
    global post_counter
    image_count = 0
    post_counter += 1
    image_name_append = []

    for j in i.find_elements_by_css_selector(get_images_div_css_selector):
        for k in BeautifulSoup(j.get_attribute('innerHTML'), 'lxml'):
            for l in k.find_all('img'):
                image_count += 1
                name_image = f'{search}/images/{post_counter}_{image_count}.jpg'
                post_image_name = f'{post_counter}_{image_count}.jpg'
                image_name_append.append(post_image_name)
                urllib.request.urlretrieve(l['src'], name_image)
    posts_dataframe_capture.append(image_name_append)

def append_to_list():
    posts_dataframe_list.append(posts_dataframe_dict.copy())
    posts_dataframe_dict.clear()

def save_to_file():
    filename = f'{search}.csv'
    sector16 = pd.DataFrame(posts_dataframe_list, columns=['title', 'timestamp', 'likes', 'love', 'care', 'wow', 'haha', 'sad', 'shares', 'images', 'comments'])
    if os.path.exists(filename):
        sector16.to_csv(os.path.join(search,filename), header=False, mode='a', index=False)
    else:
        sector16.to_csv(os.path.join(search,filename), header=False, mode='a', index=True)

    posts_dataframe_capture.clear()
    posts_dataframe_list.clear()

def scroll_to_bottom():
    driver.execute_script("window.scrollTo(window.pageYOffset, document.body.scrollHeight);")
    time.sleep(random.randint(7,13))

option = Options()

option.add_argument("--disable-infobars")
option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1
})

driver = webdriver.Chrome(
    options=option, executable_path='chromedriver.exe')
# s = f"https://facebook.com/{search}"
driver.get("https://facebook.com")
time.sleep(random.randint(2,3) + random.random())
# driver.get(s)
pyautogui.keyDown('Ctrl')
pyautogui.press('l')
pyautogui.keyUp('Ctrl')

pyautogui.press('right')
time.sleep(random.random())
pyautogui.press('/')

for i in search:
    pyautogui.press(i)
    time.sleep(random.random())

pyautogui.hotkey('enter')


# bypass()
driver.maximize_window()

no_login()

last_count_selenium = 0

while(True):
    source_selenium = selenium_source_posts()
    length_selenium = len(source_selenium)
    
    print(f'Posts to be scraped : {len(source_selenium)}')
    for source in tqdm(source_selenium[last_count_selenium:length_selenium]):
        extend_comments(source)
        get_images(source)

    source_beautiful = beautiful_source_posts(source_selenium[last_count_selenium:length_selenium])
    if(len(source_beautiful) > 0):
        for count, source in enumerate(source_beautiful):
            get_title(source)
            get_timestamp(source)
            get_reactions(source)
            get_num_shares(source)
            get_comments(source)

            posts_dataframe_dict['images'] = posts_dataframe_capture[count]

            append_to_list()

        save_to_file()
        print(f"Number of posts : {length_selenium}         Tally images post : {post_counter}")
        print('Saving to file')

        last_count_selenium = length_selenium
        length_selenium = len(source_selenium)

        if(last_count_selenium == length_selenium):
            scroll_to_bottom()
    
    time.sleep(random.randint(7,12))
