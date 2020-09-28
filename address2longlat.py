from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
import time
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
r = re.compile(r"\/@([\d\.]+),([\d\.]+),([\d]+)z\/")

def start_google_maps():
    firefox_profile = webdriver.FirefoxProfile(r"ff\Data\profile")
    firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
    binary = FirefoxBinary(r"ff\App\Firefox64\firefox.exe")
    driver = webdriver.Firefox(firefox_profile = firefox_profile, firefox_binary=binary)
    driver.get("http://maps.google.com")
    return driver

def get_long_lat_zoom(address):
    address = address.strip()
    elem = driver.find_element_by_id("searchboxinput")
    elem.clear()
    elem.send_keys(address)
    elem.send_keys(Keys.RETURN)
    current_address = driver.current_url
    matches = None
    while current_address == driver.current_url or matches is None or driver.current_url[-1] == '/':
        time.sleep(1)
        matches = r.search(driver.current_url)

    matches = r.search(driver.current_url)
    return address, matches.group(1), matches.group(2), matches.group(3)

if __name__ == "__main__":
    driver = start_google_maps()
    with open("places.txt", newline="", encoding="utf-8") as f:
        for line in f:
            address, long, lat, zoom = get_long_lat_zoom(line)
            print(f"{address}\t{long}\t{lat}\t{zoom}")
            time.sleep(1)

    driver.close()
