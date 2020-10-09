import time
import browser_extentions
from inspect import getmembers, isfunction
from selenium.webdriver.common.by import By

def extend_driver(driver_class):
    for method_name, method in [o for o in getmembers(browser_extentions) if isfunction(o[1])]:
        setattr(driver_class, method_name, method)

def tweets(browser, twitter, url):
    browser.get(url)
    browser.wait(By.XPATH, ".//div[@data-testid='reply']")
    try:
        tweet = next(twitter.get_tweets())
        twitter.like_and_retweet(tweet)
        time.sleep(1)
    except: pass