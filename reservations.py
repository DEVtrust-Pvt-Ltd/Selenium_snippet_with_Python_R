# Importing required dependencies.
import time
import os
import pickle
import undetected_chromedriver as uc
from datetime import date, timedelta
import yaml
# Login through stored cookies.

credentials = yaml.load(open('./credentials.yml','r'),Loader=yaml.FullLoader)
def Reservation(pkl_file):
    '''
    1. Here we are using pickle library to load cookies dump under pickle file.
    2. Here we are using undetected chrome browser to avoid website to identify browser agent.
    3. In case any error occurs exceed sleep time.
    '''

    last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
    start_day_of_prev_month = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)

    last_day_of_prev_month = last_day_of_prev_month.strftime('%d/%m/%Y')
    start_day_of_prev_month = start_day_of_prev_month.strftime('%d/%m/%Y')
    print(start_day_of_prev_month)
    options = uc.ChromeOptions()
    options.headless=True
    directory="Reservations_csv"
    loc=os.getcwd()
    download_dir=os.path.join(loc,directory)
    options.add_argument('--headless')
    driver = uc.Chrome(options=options)
    driver.get('https://www.air.co.in/login')

    ####################################################################################### Loading cookies through pickle file and adding it to driver #################################################################################
   
    cookies = pickle.load(open(pkl_file, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    ################################################################################################## Downloading csv file from website ################################################################################################
    try:

        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        command_result = driver.execute("send_command", params)

        driver.maximize_window()
        driver.get('https://www.air.co.in/hosting/reservations/all')
        time.sleep(10)

        driver.find_element("xpath","//button[@data-testid='toolbar_filter']").click()
        time.sleep(10)

        driver.find_element("xpath","//input[@id='startDate']").click()
        time.sleep(5)

        driver.find_element("xpath","//button[@aria-label='Go back to switch to the previous month.']").click()
        time.sleep(5)

        driver.find_element("xpath",f"//div[@data-testid='calendar-day-{start_day_of_prev_month}']").click()
        time.sleep(5)

        driver.find_element("xpath","//input[@id='endDate']").click()
        time.sleep(10)

        driver.find_element("xpath",f"//div[@data-testid='calendar-day-{last_day_of_prev_month}']").click()
        time.sleep(5)

        driver.find_element("xpath","//button[text()='Apply']").click()
        time.sleep(5)

        driver.find_element("xpath","//span[text()='Export']/parent::span[@class='_14d5b3i']/parent::button").click()
        time.sleep(10)

        driver.find_element("xpath","//button[text()='Download CSV file…']").click()
        time.sleep(10)
        
        driver.find_element("xpath","//a[text()='Download']").click()
        time.sleep(5)
        print('Downloaded sucessfully')

    except:
        print('Runtime error')


if __name__=='__main__':
    pkl_file= credentials['user_cookies']['cookies_user1']
    Reservation(pkl_file)
    