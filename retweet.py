from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
import time
import random
from datetime import datetime
import pickle
import os

def scroll(el):
    driver.execute_script("arguments[0].scrollIntoView();", el)

def click_and_wait(el, delay=1):
    el.click()
    time.sleep(delay - random.random() * delay)

binary = FirefoxBinary(r"ff\App\Firefox64\firefox.exe")
firefox_profile = webdriver.FirefoxProfile(r"ff\Data\profile")
driver = webdriver.Firefox(firefox_profile = firefox_profile, firefox_binary=binary)

driver.get("https://twitter.com/shiroihamusan")

time.sleep(5)
html = driver.find_element_by_tag_name("html")
tweets = driver.find_elements_by_xpath("//div[@data-testid='tweet']")

count = 0
last = 0
visited = {}
i = 0
while True:

    time.sleep(1)
    tweets = driver.find_elements_by_xpath("//div[@data-testid='tweet']")

    if len(tweets) <= i:
        i = 0
        scroll(tweets[i])

    tweet = tweets[i]
    date = datetime.fromisoformat(tweet.find_element_by_tag_name('time').get_attribute('datetime')[:-1])
    key = tweet.find_element_by_xpath('.//time/..').get_attribute('href')
    if key not in visited:
        visited[key] = True

        if (datetime.utcnow() - date).total_seconds() / 60 / 60 < 18:
            els = tweet.find_elements_by_xpath(".//div[@data-testid='like']")
            if len(els) > 0:
                likes = els[0]
                likes_count = 9999
                try:
                    likes_count = int(likes.get_attribute('innerText'))
                except: pass
                if likes_count > 100:
                    scroll(tweet)
                    els = tweet.find_elements_by_xpath(".//div[@data-testid='retweet']")
                    if len(els) > 0:
                        retweet = els[0]
                        click_and_wait(retweet, 0.5)
                        click_and_wait(driver.find_element_by_xpath("//div[@data-testid='retweetConfirm']"), 0.5)

                        click_and_wait(likes, 2)
                        count += 1
                        last = len(visited)

                        html.send_keys(Keys.PAGE_DOWN)
                        scroll(tweet)

    html.send_keys(Keys.PAGE_DOWN)
    i += 1
    if len(visited) > 50 or count >= 20: break

driver.close()
