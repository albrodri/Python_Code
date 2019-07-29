# -*- coding: utf-8 -*-

"""
    purpose: Webscraping Loopnet.com
    author: Alberto Rodriguez
    date: 2019+07+28
"""

import os
import re
import requests
from datetime import datetime

# Global Variables
startTime = datetime.now()
date = datetime.now().strftime('%Y+%m+%d')
os.chdir(os.path.dirname((os.path.abspath(__file__))))  # Sets the working directory to the path of the script file


def print_msg(msg):
    # TODO: Save the log message into a text file; Add the time the script is run into the name
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {msg}')


def get_api():
    # url = 'https://www.loopnet.com/for-sale/ozone-park-ny/'
    url = 'https://www.loopnet.com/for-sale/'

    url_to_parse = list()  # Will be used to store all of the returned urls for each item
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/75.0.3770.142 Safari/537.36'
    }
    params = {
        'page': 1,
        'country': 'united-states',
        'state': 'new-york',
        'city': 'brooklyn-ny',
        # 'city': 'queens-ny',
        # 'city': 'new-york-ny',
    }

    with requests.Session() as s:
        print_msg(f'Attempting to access {url}')
        # Will try to make the API GET request and store the response
        try:
            r = s.get(url, headers=hdr, params=params)
            print_msg('Success')

            # The response of the API call is HTML body of the website; Gets decoded and stored as one large string
            body_content = r.content.decode()

            # Performs scraping of the first page to identify each listing
            # print_msg('Attempting to scrape page 1')
            # url_to_parse = find_url(body_content, url_to_parse)
            # print_msg('Success')
            # print(url_to_parse)

            # Finds the max page number
            max_page_num = 1  # Sets the default value to 1
            page_num_regex = r'data-pg=\"(\d{0,10})\">'
            page_num_matches = re.finditer(page_num_regex, body_content, re.M)
            for matchNum, match in enumerate(page_num_matches, start=1):
                for groupNum in range(0, len(match.groups())):
                    groupNum += 1
                    matched_page = match.group(groupNum)

                    # Checks to see if the digit identified is greater than the one stored, by defaults its one
                    if int(matched_page) > max_page_num:
                        max_page_num = int(matched_page)

            print_msg(f'Total number of pages is {max_page_num}')

            # For each page number the script will make a call to the appropriate url and store the response
            # Then, it passes it to a function to parse out the url and append it to our list of urls
            for number in range(1, max_page_num + 1):
                params['page'] = number

                r = s.get(url, headers=hdr, params=params)
                body_content = r.content.decode()

                print_msg(f'Attempting to scrape page {number}')
                url_to_parse = find_url(body_content, url_to_parse)
                print_msg('Success')

            temp_list = list()
            for index, x in enumerate(url_to_parse):
                # r = s.get(x, headers=hdr)
                # body_content = r.content.decode()

                parse_url = re.split(r'/', x)[4:6]

                temp_dict = {
                    'url': x,
                    'title': parse_url[0],
                    'listing_id': parse_url[1],
                }

                temp_list.append(temp_dict)

            print(temp_list)

            #     # Saves the HTML information locally for the listing
            #     with open(f'{temp_dict["title"]}.txt', 'w', encoding='utf-8') as file:
            #         file.write(body_content)
            #     file.close()
            #
            # for index, x in enumerate(temp_list):
            #     print(x)

        except Exception as e:
            print(e)


def find_url(body_content, url_to_parse):
    # Declarations
    url_regex = r'\shref=\"(https://www\.loopnet\.com/Listing/.*)\"\stitle'

    url_matches = re.finditer(url_regex, body_content, re.M)

    # Used to iterate through the matched groups from the REGEX
    for matchNum, match in enumerate(url_matches, start=1):

        for groupNum in range(0, len(match.groups())):
            groupNum += 1

            matched_url = match.group(groupNum)

            if matched_url not in url_to_parse:
                url_to_parse.append(matched_url)

    return url_to_parse


def parse_page():
    print()


def elapsed_time():
    seconds = datetime.now() - startTime
    seconds = int(seconds.total_seconds())

    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    if days > 0:
        print('Total runtime for this script was %dd %dh %dm %ds' % (days, hours, minutes, seconds))
    elif hours > 0:
        print('Total runtime for this script was %dh %dm %ds' % (hours, minutes, seconds))
    elif minutes > 0:
        print('Total runtime for this script was %dm %ds' % (minutes, seconds))
    else:
        print('Total runtime for this script was %ds' % (seconds,))


# **********************************************************************************************************************
if __name__ == '__main__':

    get_api()
    elapsed_time()
