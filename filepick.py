from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import pyautogui
import time
import pandas as pd
import random
import os
import shutil

time_between_pagemove = 0.2

search_query = 'tekken'

option = Options()

option.add_argument("--disable-infobars")
option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 1 
})

driver = webdriver.Chrome(chrome_options=option, executable_path='C:\Windows\chromedriver.exe')
driver.get("https://facebook.com")

# Wait for facebook page to load
time.sleep(2)

pyautogui.keyDown('winleft')
pyautogui.press('up')
pyautogui.keyUp('winleft')

# Enter details of facebook user login and submit
login_user = driver.find_element_by_xpath('''//input[@id='email']''')
login_user.send_keys('deepak@1touch-dev.com')
time.sleep(1)
login_pass = driver.find_element_by_xpath('''//input[@id='pass']''')
login_pass.send_keys('poiuyt123')

try:
    login_button = driver.find_element_by_id('login_form')
    login_button.submit()
except:
    login_button = driver.find_element_by_css_selector('._42ft._4jy0._6lth._4jy6._4jy1.selected._51sy')
    login_button.submit()

# Wait for facebook home page to load
time.sleep(6)

# # Search in the search bar         -            Workaround in next step
# for i in range(10):
#     try:
#         search_bar = driver.find_element_by_xpath('''//div[@id='u_'''+ str(i) + '''_2']//input[@placeholder='Search']''')
#         print(f'''//div[@id='u_{i}_2']//input[@placeholder='Search']''')
#         search_bar.send_keys("https://facebook.com/" + search_query)

#     except:
#         pass

# Search the page in search bar
pyautogui.hotkey('ctrl', 'l')
time.sleep(1)
pyautogui.write('https://facebook.com/' + search_query + '/posts')
pyautogui.press('enter')

# # Get to the posts tab            -               Handled in above step
# posts_link = driver.find_element_by_xpath('''//span[contains(text(),'Posts')]''')
# posts_link.click()

time.sleep(6)

# Get the posts
while(True):
    
    post_class = driver.find_elements_by_css_selector('._4-u2._4-u8')

    posts_dataframe_list = []
    prevent_duplicate = 0
    for i in post_class:
        prevent_duplicate += 1
        if(prevent_duplicate%2==0):
            posts_dataframe_dict = dict()
            
            x = BeautifulSoup(i.get_attribute('innerHTML'), 'html.parser')
            # print(x)

        ##################### Random page downs to see more #######################
            for num in range(random.randint(5,9)):
                pyautogui.press('pagedown')
                time.sleep(time_between_pagemove)
            for num in range(random.randint(1,4)):
                time.sleep(time_between_pagemove)
                pyautogui.press('pageup')

            # WORKING CODE BELOW - UNCOMMENT AT TIME OF RUNNING              REACTIONS , COMMENTS , SHARES
            ################## Getting the title of post #####################
            for i in x.find_all('p'):
                try:
                    print(i.text)
                    posts_dataframe_dict['title'] = i.text
                except:
                    pass
                break
            ################# Getting timestamp of the post ##################
            for i in x.find_all('span',{"class":{"timestampContent"}}):
                try:
                    print(i.text)
                    posts_dataframe_dict['timestamp'] = i.text
                except:
                    pass
        # ##################### Random page downs to see more #######################
        #     for num in range(random.randint(5,9)):
        #         time.sleep(time_between_pagemove)
        #         pyautogui.press('pagedown')
        #     for num in range(random.randint(1,4)):
        #         time.sleep(time_between_pagemove)
        #         pyautogui.press('pageup')
            ################## Getting the total reactions from a post ##################
            count = 0
            for i in x.find_all('span',{"class":"_1n9k"}):
                for j in i.find_all('a'):
                    print(j['aria-label'])
                    if count == 2:
                        posts_dataframe_dict['care'] = j['aria-label']
                    if count == 1:
                        posts_dataframe_dict['love'] = j['aria-label']
                        count+=1
                    if count == 0:
                        posts_dataframe_dict['likes'] = j['aria-label']
                        count+=1
            for i in x.find_all('form'):
            
                ################## Getting the total reactions from a post ##################
                for j in i.find_all('a'):
                    for k in j.find_all('span', {"class":"_81hb"}):
                        # print(j)
                        try:
                            # print(j.text.strip()[-8:].strip())
                            print(k.text)
                            posts_dataframe_dict['total_reactions'] = k.text
                        except:
                            pass
                        break
                ################### Getting the number of comments ###################
                for j in i.find_all('a', {"class":"_3hg- _42ft"}):
                    # Will get the commnets upto 3 digits ( limit : 999k)
                    posts_dataframe_dict['commnets'] = j.text
                    print(j.text)
                    # print(j.text.strip()[0:3].strip())
                
                ################### Getting number of shares #####################
                for j in i.find_all('a', {"class":"_3rwx _42ft"}):
                    # Will get the shares upto 3 digits ( limit : 999k)
                    posts_dataframe_dict['total_reactions'] = j.text
                    print(j.text)
        ##################### Random page downs to see more #######################
            for num in range(random.randint(5,9)):
                time.sleep(time_between_pagemove)
                pyautogui.press('pagedown')
            for num in range(random.randint(1,4)):
                time.sleep(time_between_pagemove)
                pyautogui.press('pageup')                   
            
            
            posts_dataframe_list.append(posts_dataframe_dict)
            print('\n')
            print(posts_dataframe_dict)
            
    posts_dataframe = pd.DataFrame(posts_dataframe_list)

    posts_dataframe.to_csv("C:\\Users\\vaibh\\Desktop\\facebook.csv")
    print('Moving the file to backup')
    shutil.move("C:\\Users\\vaibh\\Desktop\\facebook.csv", "C:\\Users\\vaibh\\Desktop\\backup\\facebook.csv")

    time.sleep(2)