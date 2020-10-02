import time
from datetime import datetime
import os
from ff import Browser
from twitter import Twitter
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Retweet a specific page')
    parser.add_argument('--url_or_file', default='https://twitter.com/shiroihamusan')
    parser.add_argument('--max_hours', default=18, type=int)
    parser.add_argument('--min_likes', default=100, type=int)
    parser.add_argument('--posts_to_retweet', default=20, type=int)
    parser.add_argument('--posts_to_read', default=50, type=int)
    parser.add_argument('--headless', action='store_true', default=False)

    args = parser.parse_args()

    urls = [args.url_or_file]
    if os.path.exists(args.url_or_file):
        with open(args.url_or_file, newline="", encoding="utf-8") as f:
            urls = [url.strip() for url in f if len(url.strip()) > 0]
    
    with Browser(headless=args.headless) as browser:
        twitter = Twitter(browser)
        for url in urls:
            browser.driver.get(url)
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

                    # retweet those with many likes within certain period
                    if not tweet.liked and tweet.likes > args.min_likes and (datetime.utcnow() - tweet.time).total_seconds() / 60 / 60 < args.max_hours:
                        twitter.like_and_retweet(tweet)
                        tweeted += 1

                if len(visited) > args.posts_to_read or tweeted >= args.posts_to_retweet: break
                time.sleep(2)

        time.sleep(60)
