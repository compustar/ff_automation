from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
import utils

utils.extend_driver(webdriver.Firefox)

def init(url=None, private=False, executable_path=r"ff\App\Firefox64\firefox.exe", profile_path=r"ff\Data\profile", headless=False):
    firefox_profile = webdriver.FirefoxProfile(profile_path)
    if private:
        firefox_profile.set_preference("browser.privatebrowsing.autostart", True)

    options = Options()
    if headless:
        options.headless = True

    binary = FirefoxBinary(executable_path)

    driver = webdriver.Firefox(firefox_profile = firefox_profile, firefox_binary=binary, firefox_options=options)
    if url is not None:
        driver.get(url)

    return driver