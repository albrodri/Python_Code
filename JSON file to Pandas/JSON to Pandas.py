# -*- coding: utf-8 -*-
"""
    purpose: To get the results from an API call and convert to a pandas data frame
    author: Alberto Rodriguez
    date: 2019+05+18
"""

import json
import urllib.request
import urllib.parse
import pandas as pd


def call_api():
    """
    To make the GET API call

    :return: a list that contains the response from the HTTP GET call
    """

    # url = 'https://jsonplaceholder.typicode.com/comments'
    url = 'https://jsonplaceholder.typicode.com/posts'
    hdr = {
        'Content-Type': 'application/json',
    }
    params = {
        'userId': '1',
        # 'id': '2',
    }

    # Encodes the parameters and appends it to the url
    query_string = urllib.parse.urlencode(params)
    url = url + '?' + query_string

    # Create the base HTTP request
    response = urllib.request.Request(url)

    # Add the headers to the HTTP request
    for header, value in hdr.items():
        response.add_header(header, value)

    # Make the HTTP request to retrieve the JSON
    response = urllib.request.urlopen(response)

    # Read the response into a list
    data = json.loads(response.read())

    return data


if __name__ == '__main__':
    responseDf = pd.DataFrame(call_api())
    # json_results.to_csv('testing.csv', encoding='utf-8', index=False)

    print(responseDf)
