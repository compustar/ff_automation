from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
import random
import time

class Browser:
    def __init__(self, url=None, private=False, executable_path=r"ff\App\Firefox64\firefox.exe", profile_path=r"ff\Data\profile", headless=False):
        firefox_profile = webdriver.FirefoxProfile(profile_path)
        if private:
            firefox_profile.set_preference("browser.privatebrowsing.autostart", True)

        options = Options()
        if headless:
            options.headless = True

        binary = FirefoxBinary(executable_path)

        self.driver = webdriver.Firefox(firefox_profile = firefox_profile, firefox_binary=binary, firefox_options=options)
        if url is not None:
            self.driver.get(url)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.driver.quit()

    def scroll_to_element(self, element, offset=-150):
        if element is not None:
            self.driver.execute_script(f"arguments[0].scrollIntoView();window.scrollBy(0, {offset});", element)

    def click_and_wait(self, el, delay=1):
        ActionChains(self.driver).move_to_element(el).click().perform()
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

    def wait(self, by, p):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by, p))
        )
