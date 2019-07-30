# -*- coding: utf-8 -*-

"""
    purpose: Webscraping Loopnet.com
    author: Alberto Rodriguez
    date: 2019+07+28
"""

import os
import re
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

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

        # For each page number the script will make a call to that page url and store the response
        # Then, it passes it to a function that will parse out the url for each listing
        # and append it to our list of urls
        for number in range(1, max_page_num + 1):
            params['page'] = number

            r = s.get(url, headers=hdr, params=params)
            body_content = r.content.decode()

            print_msg(f'Attempting to scrape page {number}')
            url_to_parse = find_url(body_content, url_to_parse)
            print_msg('Success')

        # **************************************************************************************************************
        # By this point we have all of the listing URLS because we iterated through each page and parsed them out
        # We will now iterate over each individual listing URL and parse out the relevant information
        # TODO: Think about if we should save the HTML content of each listing and then iterate offline

        temp_list = list()

        for index, x in enumerate(url_to_parse):
            temp_dict = {}  # Creates or Resets the temporary dictionary that will hold the information for each listing
            print_msg(f'Working on {x}')

            # Makes the necessary call to get the html information
            r = s.get(x, headers=hdr)
            content = r.content.decode()
            soup = BeautifulSoup(content, 'lxml')  # Parse the HTML as a string

            # Stores the url of the page we are scraping
            temp_dict['url'] = x

            # Returns and stores the unique listing id
            try:
                listing_id = re.search('gtm-listing-id=\"(.*)\"', content, re.M).group(1)
                temp_dict['listing_id'] = listing_id
            except:
                temp_dict['listing_id'] = None

            # Returns and stores the first title
            try:
                title = soup.find('h1', class_='profile-hero-title').text
                temp_dict['title'] = title
            except:
                temp_dict['title'] = None

            # Returns and stores the first sub title
            try:
                sub_title = soup.find('h2', class_='profile-hero-sub-title').text
                temp_dict['sub_title'] = sub_title
            except:
                temp_dict['sub_title'] = None

            # Returns and stores the space use
            try:
                space_use = re.search('gtm-listing-space-use=\"(.*)\"', content, re.M).group(1)
                temp_dict['space_use'] = space_use
            except:
                temp_dict['space_use'] = None

            # Returns and stores the listing city
            try:
                address = soup.find('span', class_='inline-block wrap-padding').text.strip()
                temp_dict['address'] = address
            except:
                temp_dict['address'] = None

            # Returns and stores the listing city
            try:
                city = re.search('gtm-listing-city=\"(.*)\"', content, re.M).group(1)
                temp_dict['city'] = city
            except:
                temp_dict['city'] = None

            # Returns and stores the listing state
            try:
                state = re.search('gtm-listing-state=\"(.*)\"', content, re.M).group(1)
                temp_dict['state'] = state
            except:
                temp_dict['state'] = None

            # Returns and stores the zip code
            try:
                zip_code = re.search('gtm-listing-zip=\"(.*)\"', content, re.M).group(1)
                temp_dict['zip_code'] = zip_code
            except:
                temp_dict['zip_code'] = None

            # Returns and stores the listing status
            try:
                status = re.search('gtm-listing-status=\"(.*)\"', content, re.M).group(1)
                temp_dict['status'] = status
            except:
                temp_dict['status'] = None

            # Returns and stores if the listing is out of date
            try:
                out_of_date = re.search('\"IsListingOutOfDate\":([a-zA-Z].*)},\"', content, re.M).group(1)
                temp_dict['out_of_date'] = out_of_date
            except:
                temp_dict['out_of_date'] = None

            # Returns and stores the date the listing was created
            try:
                date_created = soup.find('span', text='Date Created:').next_sibling
                temp_dict['date_created'] = date_created
            except:
                temp_dict['date_created'] = None

            # Returns and stores the last modified date
            try:
                modified_date = re.search(r'\"ModifiedDate\":\"([\d\/\d\/\d]{0,10})', content, re.M).group(1)
                temp_dict['modified_date'] = modified_date
            except:
                temp_dict['modified_date'] = None

            # Returns the table that lists out the details of the property e.g. price, unit size, etc...
            try:
                table = soup.find('table', class_='property-data featured-grid')
                rows = table.find_all('tr')

                for x in range(0, len(rows)):  # Iterates through every row within the table
                    column_count = len(rows[x].find_all('td'))  # Stores the number of columns within the row
                    cols = rows[x].find_all('td')  # Returns all of the cells within the row as an object

                    for y in range(0, column_count,
                                   2):  # Iterate through the row specifically, each column in steps of 2
                        if len(cols[y].text.strip()) > 1:  # Ensure we do not include blank cells
                            temp_dict[cols[y].text.strip()] = cols[
                                y + 1].text.strip()  # Store the data in key value pairs
            except:
                continue

            # Returns and stores the sale notes
            try:
                sale_notes = soup.find('div', class_='column-12 sales-notes-text').get_text().strip()
                temp_dict['sale_notes'] = sale_notes
            except:
                temp_dict['sale_notes'] = None

            # Returns and stores the description
            try:
                description = soup.find('div', class_='column-12 description-text').get_text().strip()
                temp_dict['description'] = description
            except:
                temp_dict['description'] = None

            # Appends the pages details to a running list
            # Dictionary should be reset on the next loops iteration and populated with the new pages information
            temp_list.append(temp_dict)

    # Exports the parsed details locally
    pd.DataFrame(temp_list).to_csv('test_output.csv', index=False)


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


def save_html_locally(url, title):
    # Saves the HTML information locally for the listing
    with open(f'{temp_dict["title"]}.txt', 'w', encoding='utf-8') as file:
        file.write(body_content)
    file.close()


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
