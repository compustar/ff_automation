from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import random
import time

class Browser:
    def __init__(self, url, private=False):
        firefox_profile = webdriver.FirefoxProfile(r"ff\Data\profile")
        if private:
            firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
        binary = FirefoxBinary(r"ff\App\Firefox64\firefox.exe")
        self.driver = webdriver.Firefox(firefox_profile = firefox_profile, firefox_binary=binary)
        self.driver.get(url)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.driver.quit()

    def scroll_to_element(self, element):
        if element is not None:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def click_and_wait(self, el, delay=1):
        el.click()
        time.sleep(delay - random.random() * delay / 2)

    def scroll_by_pixel(self,  pixel):
        self.driver.execute_script(f"window.scrollBy(0,{pixel})");

    def page_down(self):
        page = self.driver.find_element_by_tag_name("body")
        page.send_keys(Keys.PAGE_DOWN)

    def is_element_visible_in_viewpoint(self, element):
        if element is None: return False
        return self.driver.execute_script("var elem = arguments[0],                 " 
                                    "  box = elem.getBoundingClientRect(),    " 
                                    "  cx = box.left + box.width / 2,         " 
                                    "  cy = box.top + box.height / 2,         " 
                                    "  e = document.elementFromPoint(cx, cy); " 
                                    "for (; e; e = e.parentElement) {         " 
                                    "  if (e === elem)                        " 
                                    "    return true;                         " 
                                    "}                                        " 
                                    "return false;                            "
                                    , element)