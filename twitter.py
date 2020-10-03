from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import ff

class Tweet():
    def __init__(self, tweet):
        self.element = tweet
        time = tweet.find_elements_by_tag_name('time')
        if len(time) > 0:
            self.time = datetime.fromisoformat(tweet.find_element_by_tag_name('time').get_attribute('datetime')[:-1])
            self.url = tweet.find_element_by_xpath('.//time/..').get_attribute('href')
            self.__parse_common__(tweet, lambda : self.like_button)

        else:
            tweet = tweet.find_element_by_xpath("./following-sibling::div")
            data = tweet.find_elements_by_xpath(".//a[starts-with(@href, '/') and span and not(starts-with(text(), '#')) and not(starts-with(span/text(), '@'))]")
            self.element = tweet
            try:
                self.time = datetime.strptime(data[0].get_attribute("innerText"), "%I:%M %p · %b %d, %Y")
            except:
                print(data[0].get_attribute("innerText"))
            self.url = data[0].get_attribute("href")
            self.__parse_common__(tweet, lambda: data[-1].find_element_by_tag_name("div"))

    def __parse_common__(self, tweet, get_likes_element):
        self.liked = len(tweet.find_elements_by_xpath(".//div[@data-testid='like']")) == 0
        self.like_button = None
        self.retweet_button = None

        if not self.liked:
            self.like_button = tweet.find_element_by_xpath(".//div[@data-testid='like']")
            if len(tweet.find_elements_by_xpath(".//div[@data-testid='retweet']")) > 0:
                self.retweet_button = tweet.find_element_by_xpath(".//div[@data-testid='retweet']")

            self.likes = get_likes_element().get_attribute('innerText')
            try:
                self.likes = int(self.likes)
            except:                
                if len(self.likes.strip()) == 0:
                    self.likes = 0
                else:
                    print(self.likes)
                    unit = self.likes[-1]
                    self.likes = float(self.likes[:-1])
                    if unit == 'K': self.likes *= 1000
                    if unit == 'M': self.likes *= 1_000_000

class Twitter():

    def __init__(self, browser, direct_line=False):
        self.browser = browser
        self.driver = browser.driver

    def like_and_retweet(self, tweet):

        if tweet.retweet_button is not None:
            if not self.browser.is_element_visible_in_viewpoint(tweet.retweet_button):
                self.browser.scroll_to_element(tweet.element)
            if not self.browser.is_element_visible_in_viewpoint(tweet.retweet_button):
                self.browser.scroll_to_element(tweet.retweet_button, -300)
            self.browser.click_and_wait(tweet.retweet_button, 0.5)
            self.confirm_retweet()

        if tweet.like_button is not None:
            if not self.browser.is_element_visible_in_viewpoint(tweet.like_button):
                self.browser.scroll_to_element(tweet.element)
            if not self.browser.is_element_visible_in_viewpoint(tweet.like_button):
                self.browser.scroll_to_element(tweet.like_button, -300)
            self.browser.click_and_wait(tweet.like_button, 2)

    def confirm_retweet(self):
        self.browser.click_and_wait(self.driver.find_element_by_xpath("//div[@data-testid='retweetConfirm']"), 0.5)

    def get_tweets(self):
        prev_first_tweet = None
        prev_tweet = None
        i = 0
        self.browser.wait(By.XPATH, "//div[@data-testid='tweet']")

        # infinite scroll
        while True:
            try:
                tweets = [Tweet(t) for t in self.driver.find_elements_by_xpath("//div[@data-testid='tweet']")]
                # tweets got refreshed... find the next tweet
                if prev_first_tweet != tweets[0].url:
                    prev_first_tweet = tweets[0].url
                    for i, t in enumerate(tweets):
                        if tweets[i].url == prev_tweet:
                            break

                    if i + 1 == len(tweets):
                        i = 0
                    else:
                        i += 1
                    self.browser.scroll_to_element(tweets[i].element)
            except StaleElementReferenceException: 
                print("Cannot get the tweets properly... retrying")
                continue


            # no scroll no new tweet
            if i >= len(tweets):
                self.browser.page_down()
                continue

            tweet = tweets[i]
            prev_tweet = tweet.url
            yield tweet
            i += 1
