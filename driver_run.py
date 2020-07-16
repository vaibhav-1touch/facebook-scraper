from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import pyautogui
import random


search = "DonaldTrump"



# Global variables
post_class_css_selector = "._5pcr.userContentWrapper"
comment_class_css_selector = "._7a94._7a9d"
get_title_div_dict = {"data-testid":"post_message"}
get_timestamp_span_dict = {"class": "timestampContent"}
get_reactions_span_dict = {"class": "_1n9k"}
get_comments_span_dict = {"class": "_3l3x"}

posts_dataframe_dict = {}
posts_dataframe_list = []

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
    for j in i.find_all('span', get_timestamp_span_dict):
        posts_dataframe_dict["timestamp"] = j.text

def get_reactions(i):
    count = 0
    for j in i.find_all('span', get_reactions_span_dict):
        for k in j.find_all('a'):
            if count == 2:
                posts_dataframe_dict['care'] = k['aria-label']
            if count == 1:
                posts_dataframe_dict['love'] = k['aria-label']
                count += 1
            if count == 0:
                posts_dataframe_dict['likes'] = k['aria-label']
                count += 1

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

def append_to_list():
    posts_dataframe_list.append(posts_dataframe_dict.copy())
    posts_dataframe_dict.clear()

def save_to_file():
    sector16 = pd.DataFrame(posts_dataframe_list)
    sector16.to_csv('facebook.csv', index=False, mode='a')
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
    options=option, executable_path='/usr/share/chromedriver')
s = f"https://facebook.com/{search}/posts"
driver.get(s)
driver.maximize_window()

no_login()

last_count_selenium = 0

while(True):

    source_selenium = selenium_source_posts()
    length_selenium = len(source_selenium)
    
    for source in source_selenium[last_count_selenium:length_selenium]:
        extend_comments(source)
    
    source_beautiful = beautiful_source_posts(source_selenium[last_count_selenium:length_selenium])
    print(len(source_beautiful))
    if(len(source_beautiful) > 0):
        for source in source_beautiful:
            get_title(source)
            get_timestamp(source)
            get_reactions(source)
            get_comments(source)

            append_to_list()

        save_to_file()
        print(f"Number of posts : {length_selenium}")
        print('Saving to file')

        last_count_selenium = length_selenium
        length_selenium = len(source_selenium)

        if(last_count_selenium == length_selenium):
            scroll_to_bottom()
    
    time.sleep(random.randint(7,12))