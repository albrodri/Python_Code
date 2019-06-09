# -*- coding: utf-8 -*-

"""
    purpose: To get the results from an API call and generate a SQL Command to store the data
    author: Alberto Rodriguez
    date: 2019+06+01
"""

import os
import pyodbc
import requests
import pandas as pd
from datetime import datetime

# Global Variables
startTime = datetime.now()
date = datetime.now().strftime('%Y+%m+%d')
os.chdir(os.path.dirname((os.path.abspath(__file__))))  # Sets the working directory to the path of the script file
fileName = 'testdb'


def print_msg(msg):
    # TODO: Save the log message into a text file; Add the time the script is run into the name
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {msg}')


def print_exception(exception):
    print_msg(exception)
    exit(1)


def get_api():
    # url = 'https://jsonplaceholder.typicode.com/photos'
    # url = 'https://jsonplaceholder.typicode.com/comments'
    url = 'https://jsonplaceholder.typicode.com/posts'
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/74.0.3729.169 Safari/537.36',
        'Content-Type': 'application/json',
    }
    params = {
        'userId': '1'
    }

    with requests.Session() as s:
        print_msg(f'Attempting to access {url}')
        # Will try to make the API GET request and store the JSON response
        try:
            r = s.get(url, headers=hdr, params=params)
            print_msg('Success')

            api_json_response = r.json()  # If the response is nested, handle it here using api_json_response['name']

        except Exception as e:
            print_exception(e)

        formatted_response = []  # Empty list to store each row of data

        # Loop will go through the response and parse it into a list then, save it as a pandas data frame
        for counter, value in enumerate(api_json_response):
            formatted_response.append(value)

        try:
            dFrame = pd.DataFrame(formatted_response)  # Convert the list to a pandas data frame
            dFrame.to_csv(f'{date}_{fileName}.csv', index=False)  # Saves the file locally
            print_msg('Saved file locally.')

        except Exception as e:
            print_exception(e)

        # Pass the data to be saved to the SQL Server Sandbox including the file name that will be used as the table
        load_data_to_db(formatted_response, 'test_db')


def load_data_to_db(data, tableName):
    # Necessary parameters to make the connection
    con = pyodbc.connect(
        Trusted_Connection='yes',
        driver='{SQL Server}',
        server=r'DESKTOP-JQ3I8KK\SQLEXPRESS',
        autocommit=True)

    cursor = con.cursor()  # Cursor object to execute SQL Commands
    xdbName = 'Database1'
    xtblName = f'{xdbName}.dbo.{tableName}'

    def create_table():
        # Next couple of lines will manipulate the column names to be MS SQL ready, see format below:
        # [col name] VarChar(col length)
        unique_column_names = []

        for counter, value in enumerate(data):
            for key in value.keys():
                col_name = f'[{key}] VARCHAR(max)'
                # col_name = col_name.lower()

                if col_name not in unique_column_names:  # Avoids duplication of the column names
                    unique_column_names.append(col_name)  # Adds the unique value, formatted column to the list

        print_msg(f'Attempting to create {xtblName}.')
        # Tries to put together the SQL command to create the table dynamically
        try:
            sql = f'DROP TABLE IF EXISTS {xtblName}; ' \
                f'CREATE TABLE {xtblName}({", ".join(col for col in unique_column_names)})'
            cursor.execute(sql)
            print_msg(f'{sql}.')
            print_msg(f'Successfully created {xtblName}.')

        except Exception as e:
            print_exception(e)

    def insert_query():
        # Tries to create and execute the insert statement for MSSQL
        try:
            for counter, value in enumerate(data):
                # Created this step to deal with special characters that may cause the SQL to fail
                tempList = []  # Used to store the manipulated values
                for words in value.values():
                    words = str(words).replace("'", "\'\'")  # Replaces single ' with double; escape char for MSSQL
                    tempList.append(words)  # Keeps a running list of manipulated words

                # will store the columns and values needed to dynamically make the SQL insert statement
                columns = (', '.join([key for key, information in value.items()]))
                values = (", ".join([f'\'{str(information)}\'' for information in tempList]))

                sql = f'INSERT INTO {xtblName} ({columns}) VALUES ({values})'
                cursor.execute(sql)
                print_msg(f'Successfully updated {xtblName} {sql}.')

        except Exception as e:
            print_exception(e)

        print_msg(f'Inserted {counter+1} rows into {xtblName}\n')

    # Tries to create the table and load the data into the SQL table
    try:
        create_table()
        insert_query()

    except Exception as e:
        print_exception(e)


def elapsed_time():
    seconds = datetime.now() - startTime
    seconds = int(seconds.total_seconds())

    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    if days > 0:
        print_msg('Total runtime for this script was %dd %dh %dm %ds' % (days, hours, minutes, seconds))
    elif hours > 0:
        print_msg('Total runtime for this script was %dh %dm %ds' % (hours, minutes, seconds))
    elif minutes > 0:
        print_msg('Total runtime for this script was %dm %ds' % (minutes, seconds))
    else:
        print_msg('Total runtime for this script was %ds' % (seconds,))


# **********************************************************************************************************************
if __name__ == '__main__':

    get_api()
    elapsed_time()
