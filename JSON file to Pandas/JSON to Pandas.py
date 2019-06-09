# -*- coding: utf-8 -*-
"""
    purpose: To get the results from an API call and convert to a pandas data frame
    author: Alberto Rodriguez
    date: 2019+05+18
"""

import json
import requests
import pandas as pd


def call_api():
    """
    To make the GET API call

    :return: a list that contains the response from the HTTP GET call
    """

    with requests.Session() as session:
        # url = 'https://jsonplaceholder.typicode.com/comments'
        url = 'https://jsonplaceholder.typicode.com/posts'
        hdr = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/74.0.3729.169 Safari/537.36',
            'Content-Type': 'application/json',
        }
        params = {
            'userId': '1',
            # 'id': '2',
        }

        r = session.get(url, headers=hdr, params=params)
        api_json_response = r.json()

        formatted_response = []

        for counter, value in enumerate(api_json_response):
            formatted_response.append(value)

            unique_headers = []
            for item in value:
                if item not in unique_headers:
                    item = item + ' varchar(255),'
                    unique_headers.append(item)

        print(unique_headers)
        # print(formatted_response)


if __name__ == '__main__':
    call_api()
