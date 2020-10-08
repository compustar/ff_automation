from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
import time

def scroll_to_element(self, element, offset=-150):
    if element is not None:
        self.execute_script(f"arguments[0].scrollIntoView();window.scrollBy(0, {offset});", element)

def click_and_wait(self, el, delay=1):
    ActionChains(self).move_to_element(el).click().perform()
    time.sleep(delay - random.random() * delay / 2)

def scroll_by_pixel(self,  pixel):
    self.execute_script(f"window.scrollBy(0,{pixel})");

def page_down(self):
    page = self.find_element_by_tag_name("body")
    page.send_keys(Keys.PAGE_DOWN)

def is_element_visible_in_viewpoint(self, element):
    if element is None: return False
    return self.execute_script("var elem = arguments[0],                 " 
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
    return WebDriverWait(self, 10).until(
        EC.presence_of_element_located((by, p))
    )