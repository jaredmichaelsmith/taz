#!/usr/bin/env python

""" fetch_all_subreddits.py - Gathers metadata of all subreddits currently on Reddit """

__author__ = "Rob Knight, Gavin Huttley, and Peter Maxwell"
__copyright__ = "Copyright 2007, The Cogent Project"
__license__ = "MIT"

import json
import csv
import time
import requests


def write_to_csv(subreddit_writer, parsed_json):
    for subreddit_data in parsed_json['data']['children']:
        subreddit_data = subreddit_data['data']
        display_name = subreddit_data['display_name']
        url = subreddit_data['url']
        subscribers = subreddit_data['subscribers']
        subreddit_type = subreddit_data['subreddit_type']
        lang = subreddit_data['lang']

        subreddit_writer.writerow({'display_name': display_name, 'url': url, 'subscribers': subscribers, 'subreddit_type': subreddit_type, 'lang': lang})


def main():
    base_url = "https://www.reddit.com/reddits/.json"
    limit = 100
    delay = 2

    user_agent_firefox = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'
    user_agent_scraper = 'Subreddit Scraper script by /u/scubasteve225 v 1.0. Url: github.com/jaredmichaelsmith'

    headers = {'user-agent': user_agent_scraper}

    with open('subreddits.csv', 'wb') as srfile:
        fieldnames = ['display_name', 'url', 'subscribers', 'subreddit_type', 'lang']
        subreddit_writer = csv.DictWriter(srfile, fieldnames=fieldnames)
        subreddit_writer.writeheader()

        after_param = None
        resp = requests.get(base_url + "?limit=100", headers=headers)
        parsed_json = json.loads(resp.text)
        after_param = parsed_json['data']['after']

        write_to_csv(subreddit_writer, parsed_json)

        while True:
            if after_param is None:
                break

            pagination_url = "{}?limit={}&after={}".format(base_url, limit, after_param)
            time.sleep(delay)
            resp = requests.get(pagination_url, headers=headers)

            parsed_json = json.loads(resp.text)
            after_param = parsed_json['data']['after']

            write_to_csv(subreddit_writer, parsed_json)


if __name__ == "__main__":
    main()
