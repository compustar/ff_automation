from selenium.webdriver.common.keys import Keys
import time
import re
import sys
import ff

sys.stdout.reconfigure(encoding='utf-8')
r = re.compile(r"\/@([\d\.]+),([\d\.]+),([\d]+)z\/")

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
    with ff("http://maps.google.com", private=True) as driver:
        with open("places.txt", newline="", encoding="utf-8") as f:
            for line in f:
                address, long, lat, zoom = get_long_lat_zoom(line)
                print(f"{address}\t{long}\t{lat}\t{zoom}")
                time.sleep(1)
