# -*- coding: utf-8 -*-
"""
    purpose: To get the results from an API call and convert to a pandas data frame
    author: Alberto Rodriguez
    date: 2019+05+18
"""

import os
import re
import pandas as pd
from datetime import datetime


# Global Variable
home_path = r'E:\Books'
date = datetime.now().strftime('%Y+%m+%d')
os.chdir(os.path.dirname((os.path.abspath(__file__))))  # Sets the working directory to the path of the script file

def main():
    """
    To make the GET API call

    :return: a list that contains the response from the HTTP GET call
    """

    file_list = []
    p = re.compile(r'^.*\.(.*)$')

    for folder, dirs, files in os.walk(home_path):
        for book_name in files:
            match = p.match(book_name)

            if match:
                file_list.append({
                    'name': book_name,
                    'extension': match.group(1),
                    'full_path': f'{folder}\{book_name}',
                })

            else:
                print('no match')
                file_list.append({
                    'name': book_name,
                    'extension': 'ERROR',
                    'full_path': f'{folder}\{book_name}',
                })

    pd.DataFrame(file_list).to_excel(f'{date} - book_inventory.xlsx',
                                     index=False,
                                     sheet_name='library_inventory',
                                     columns=['name', 'extension', 'full_path'])


if __name__ == '__main__':
    main()
