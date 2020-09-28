from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import random
import time

def start(url, private=False):
    firefox_profile = webdriver.FirefoxProfile(r"ff\Data\profile")
    if private:
        firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
    binary = FirefoxBinary(r"ff\App\Firefox64\firefox.exe")
    driver = webdriver.Firefox(firefox_profile = firefox_profile, firefox_binary=binary)
    driver.get(url)
    return driver

def scroll(driver, el):
    driver.execute_script("arguments[0].scrollIntoView();", el)

def click_and_wait(el, delay=1):
    el.click()
    time.sleep(delay - random.random() * delay / 2)

