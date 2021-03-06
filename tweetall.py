from twitter import Twitter
from ff import init as browser_init
import argparse
import re
import time
import utils

parser = argparse.ArgumentParser(description='Retweet all tweets in a file')
parser.add_argument('tweet_list', nargs='?', default='tweet_list.txt')
parser.add_argument('--headless', action='store_true', default=False)
parser.add_argument('--executable_path', default=r"ff\App\Firefox64\firefox.exe")
parser.add_argument('--profile_path', default=r"ff\Data\profile")

args = parser.parse_args()

regex = re.compile(r"https://(?:www\.)?twitter\.com[^\s]+")
with open(args.tweet_list, encoding="utf-8") as f:
    with browser_init(executable_path=args.executable_path, profile_path=args.profile_path, headless=args.headless) as browser:
        twitter = Twitter(browser)
        for line in f:
            for url in regex.findall(line):
                utils.tweets(browser, twitter, url)