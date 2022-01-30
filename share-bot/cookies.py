import os
import requests
import json
import time

from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import *
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *

true = True
false = False

def login_into_rk(cookies, password, appid, rkid):
    try:
        def get_chromedriver(proxy, use_proxy=False,  user_agent=None):

            chrome_options = webdriver.ChromeOptions()
            experimentalFlags = ['same-site-by-default-cookies@1','cookies-without-same-site-must-be-secure@1']
            chromeLocalStatePrefs = { 'browser.enabled_labs_experiments' : experimentalFlags}
            chrome_options.add_experimental_option('localState',chromeLocalStatePrefs)
            chrome_options.add_argument('--disable-notifications')


            if user_agent:
                chrome_options.add_argument('--user-agent=%s' % user_agent)
            driver = webdriver.Chrome('chromedriver.exe',
                chrome_options=chrome_options)

            return driver

        cookies = json.loads(cookies)
        print('loaded cookies')

        driver = get_chromedriver(0)
        driver.get('https://facebook.com/')


        try:
            driver.get('https://facebook.com/')
            for i in cookies:
                try:
                    print('ad cookies: ')
                    print(i)
                    driver.add_cookie(i)
                except Exception as e: print(e)
        except Exception as e: print(e)


        driver.refresh()

        try:
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div/div/div[1]/div[4]/div[1]/div/div/a[1]/div').click()
            driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div/div/form/div[2]/div/input').send_keys('Ruttur123$$$\n')
        except Exception as e:
            print(e)

        time.sleep(10)

        driver.get(f'https://developers.facebook.com/apps/{appid}/settings/advanced/')

        try:
            time.sleep(10)
            driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div/div/div/div[3]/button[2]').click()
        except Exception as e:
            print(e)

        acc_id = rkid
        time.sleep(10)

        try:
            for i in acc_id:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/div[5]/div[2]/div[2]/div/div/form/div[8]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[2]/div/div/div/div[1]/div/div/div/div/input")))
                driver.find_element_by_xpath('/html/body/div[1]/div[5]/div[1]/div/div[5]/div[2]/div[2]/div/div/form/div[8]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[2]/div/div/div/div[1]/div/div/div/div/input').send_keys(i + '\n')
        except Exception as e:
            print(e)

        time.sleep(5)

        driver.quit()
        return [1]

    except Exception as e:
        return [e]
