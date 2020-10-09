from selenium.webdriver.common.keys import Keys
import time
import re
import sys
from ff import init as browser_init
import argparse

sys.stdout.reconfigure(encoding='utf-8')
r = re.compile(r"\/@([\d\.]+),([\d\.]+),([\d]+)z\/")

def get_long_lat_zoom(driver, address):
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
    parser = argparse.ArgumentParser(description='Find the GPS info from a list of addresses')
    parser.add_argument('places_file', nargs='?', default="places.txt")
    args = parser.parse_args()

    with browser_init("http://maps.google.com", private=True) as browser:
        with open(args.places_file, newline="", encoding="utf-8") as f:
            for line in f:
                address, long, lat, zoom = get_long_lat_zoom(browser, line)
                print(f"{address}\t{long}\t{lat}\t{zoom}")
                time.sleep(1)
