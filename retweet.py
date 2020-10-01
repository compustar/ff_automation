import time
from datetime import datetime
import os
from ff import Browser
from twitter import Twitter
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Retweet a specific page')
    parser.add_argument('--url_or_file', default='https://twitter.com/shiroihamusan')
    parser.add_argument('--retweet_less_than_hours', default=18, type=int)
    parser.add_argument('--headless', action='store_true', default=False)

    args = parser.parse_args()

    url = args.url_or_file
    if os.path.exists(url):
        with open(url, newline="", encoding="utf-8") as f:
            url = f.readline().strip()

    with Browser(url, headless=args.headless) as browser:
        twitter = Twitter(browser)
        time.sleep(5)

        visited = {}
        tweeted = 0
        for tweet in twitter.get_tweets():
            for i in range(2):
                if tweet.retweet_button is None or browser.is_element_visible_in_viewpoint(tweet.retweet_button): break
                browser.page_down()

            key = tweet.url
            if key not in visited:
                visited[key] = True

                # retweet those with less than 18 hours
                if (datetime.utcnow() - tweet.time).total_seconds() / 60 / 60 < args.retweet_less_than_hours:                    
                    if not tweet.liked and tweet.has_many_likes():
                        twitter.like_and_retweet(tweet)
                        tweeted += 1

            if len(visited) > 50 or tweeted >= 20: break
            time.sleep(2)

        time.sleep(60)
