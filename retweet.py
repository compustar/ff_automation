import time
from datetime import datetime
import pickle
import os
import ff

class Tweet():
    def __init__(self, tweet):
        self.element = tweet
        self.time = datetime.fromisoformat(tweet.find_element_by_tag_name('time').get_attribute('datetime')[:-1])
        self.url = tweet.find_element_by_xpath('.//time/..').get_attribute('href')
        self.liked = len(tweet.find_elements_by_xpath(".//div[@data-testid='like']")) == 0
        self.like_button = None
        self.retweet_button = None

        if not self.liked:
            self.like_button = tweet.find_element_by_xpath(".//div[@data-testid='like']")
            self.retweet_button = tweet.find_element_by_xpath(".//div[@data-testid='retweet']")

            self.likes = self.like_button.get_attribute('innerText')
            try:
                self.likes = int(self.likes)
            except: pass

    def has_many_likes(self):
        return not self.liked and (type(self.likes) == str or self.likes > 100)

class TwitterBrowser(ff.Browser):
    def like_and_retweet(self, tweet):
        if not self.is_element_visible_in_viewpoint(tweet.retweet_button):
            self.scroll_to_element(tweet)
        self.click_and_wait(tweet.retweet_button, 0.5)
        self.confirm_retween()
        self.click_and_wait(tweet.like_button, 2)

    def confirm_retween(self):
        self.click_and_wait(self.driver.find_element_by_xpath("//div[@data-testid='retweetConfirm']"), 0.5)

    def get_tweets(self):
        return [Tweet(tweet) for tweet in self.driver.find_elements_by_xpath("//div[@data-testid='tweet']")]

if __name__ == "__main__":
    with TwitterBrowser("https://twitter.com/shiroihamusan") as browser:
        time.sleep(5)
        tweets = browser.get_tweets()

        tweeted = 0
        visited = {}
        prev_first_tweet = None
        prev_tweet = None
        i = 0
        while True:
            tweets = browser.get_tweets()

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
                browser.scroll_to_element(tweets[i].element)

            tweet = tweets[i]
            prev_tweet = tweet.url

            for i in range(2):
                if browser.is_element_visible_in_viewpoint(tweet.retweet_button): break
                browser.page_down()

            key = tweet.url
            if key not in visited:
                visited[key] = True

                # retweet those with less than 18 hours
                if (datetime.utcnow() - tweet.time).total_seconds() / 60 / 60 < 18:                    
                    if not tweet.liked and tweet.has_many_likes():
                        browser.like_and_retweet(tweet)
                        tweeted += 1

            i += 1
            if len(visited) > 50 or tweeted >= 20: break
            time.sleep(1)

        time.sleep(60)
