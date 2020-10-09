import time
from datetime import datetime
import os
from twitter import Twitter
from ff import init as browser_init
import argparse
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import urllib.parse
import utils

parser = argparse.ArgumentParser(description='Retweet links in twitter helper bot')
parser.add_argument('--headless', action='store_true', default=False)
parser.add_argument('--executable_path', default=r"ff\App\Firefox64\firefox.exe")
parser.add_argument('--profile_path', default=r"ff\Data\profile")

args = parser.parse_args()

with browser_init("https://web.telegram.org/#/im?p=@TwitterHelpBot", executable_path=args.executable_path, profile_path=args.profile_path, headless=args.headless) as browser:
    browser.wait(By.CLASS_NAME, "composer_rich_textarea")
    time.sleep(5)
    input = browser.find_element_by_class_name("composer_rich_textarea")
    input.send_keys("/task")
    input.send_keys(Keys.ENTER)
    time.sleep(2)
    browser.wait(By.XPATH, "//button[text()='香港直擊...']")
    browser.find_elements_by_xpath("//button[text()='香港直擊...']")[-1].click()
    time.sleep(5)
    twitter = Twitter(browser)
    for url in [a.get_attribute('href') for a in browser.find_elements_by_xpath("(//div[@class='im_message_text'])[last()]/a")[:-1]]: 
        url = urllib.parse.unquote(re.search('url=(.+)', url).group(1))
        utils.tweets(browser, twitter, url)