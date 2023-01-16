# Importing required dependencies
import time
import pickle
import undetected_chromedriver as uc
import os
import yaml

# loading .yml file
credentials = yaml.load(open('./credentials.yml','r'),Loader=yaml.FullLoader)

# Load credentials of users of which you want to generate pickle file. 
user1=credentials['login_credentials']['user1']
pass1=credentials['login_credentials']['pass1']
user2=credentials['login_credentials']['user2']
pass2=credentials['login_credentials']['pass2']



def saving_cookies(username,password):
    '''
    Note: 
    1. For first time we need to login using credentials.This is for saving site cookies.
    2. We are storing this cookies in pickle file and reuse it for our login purpose. 
    '''
    try:
        
        options = uc.ChromeOptions()
        options.headless=True
        options.add_argument('--headless')
        driver = uc.Chrome(options=options)

        driver.get('https://www.air.co.in/login')
        time.sleep(8)

        driver.find_element_by_xpath("//div[text()='Continue with email']/ancestor::button").click()
        time.sleep(10)

        driver.find_element_by_xpath("//input[@name='user[email]']").send_keys(username)
        time.sleep(10)

        driver.find_element_by_xpath("//span[text()='Continue']/ancestor::button").click()
        time.sleep(10)

        driver.find_element_by_xpath("//input[@name='user[password]']").send_keys(password)
        time.sleep(10)

        driver.find_element_by_xpath("//span[text()='Log in']/ancestor::button").click()
        time.sleep(20)

        pickle.dump(driver.get_cookies(), open(username+'.pkl', "wb"))

    except:
        print('Runtime Error')


# We need to pass arguments username and password of which we want to store cookies in pickle file. 
if __name__=='__main__':
    saving_cookies(user1,pass1)
