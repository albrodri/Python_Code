# -*- coding: utf-8 -*-
"""
    purpose: To get the results from an API call and convert to a pandas data frame
    author: alberto rodriguez
    date: 2018+12+26
"""

import requests
import pandas as pd


def callApi():

    url = 'https://jsonplaceholder.typicode.com/comments' # should be 500
    headers = {
        'Content-Type': 'application/json'
    }

    returned_results = requests.get(url, headers=headers)

    return returned_results.content


if __name__ == '__main__':

    json_results = pd.read_json(callApi(), orient='columns')
    json_results.to_csv('testing.csv', encoding='utf-8', index=False)
