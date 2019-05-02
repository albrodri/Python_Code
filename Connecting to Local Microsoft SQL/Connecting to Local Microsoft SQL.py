# -*- coding: utf-8 -*-
"""
Created on Fri April 26 19:32:44 2019

@author: Alberto Rodriguez
"""

import os
import pyodbc
import logging
from datetime import datetime


# Necessary parameters to make the connection
con = pyodbc.connect(
    Trusted_Connection='yes',
    driver='{SQL Server}',
    server=r'DESKTOP-JQ3I8KK\SQLEXPRESS',
    autocommit=True)


# Global Variables
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Sets working directory to folder the script is being run from
logging.basicConfig(filename='Connecting to Local SQL DB Logs.log', level=logging.DEBUG)  # The name of the log file
start_time = datetime.now()
cursor = con.cursor()  # Cursor object to execute SQL Commands
xdbName = 'Database1'
xtblName = f'{xdbName}.dbo.dummy1'


def create():
    """
    Will create the database and the table for this example

    :return:
    """
    print_save_log(f'Attempting to create database {xdbName}')
    try:
        sql = f'CREATE DATABASE {xdbName}'
        cursor.execute(sql)
        print_save_log('Success')
    except Exception as e:
        print_save_log(e)
        pass

    print_save_log(f'Attempting to create table {xtblName}')
    try:
        sql = f'CREATE TABLE {xtblName} (id INT, name VARCHAR(50))'
        cursor.execute(sql)
        print_save_log('Success')
    except Exception as e:
        print_save_log(e)
        pass


def insert():
    """
    Adds information to our table within the database created by the python script

    :return:
    """
    print_save_log(f'Attempting to insert python list into {xtblName}')
    superHeroNames = [
        {id: 97, 'name': 'Logan'},
        {id: 84, 'name': 'Rosanna'},
        {id: 54, 'name': 'Iron Man'},
        {id: 96, 'name': 'Captain America'},
        {id: 65, 'name': 'Thor'},
        {id: 23, 'name': 'Hulk'},
        {id: 14, 'name': 'Deadpool'},
        {id: 87, 'name': 'Thing'},
        {id: 1, 'name': 'John Constantine'},
        {id: 8, 'name': 'Aquaman'},
    ]
    print_save_log(superHeroNames)

    # Will iterate through each key/value pair in the superHeroNames list and insert into sql table
    for row in superHeroNames:
        sql = f'INSERT INTO {xtblName} (id, name) VALUES (?, ?)'
        val = (row[id], row['name'])
        cursor.execute(sql, val)

    print_save_log('Success')
    read()  # Function to read the table


def delete():
    """
    Will delete values from the table within the database

    :return:
    """


def read():
    """
    Shows all values currently in the table

    :return:
    """
    sql = f'SELECT * FROM {xtblName}'
    data = cursor.execute(sql)

    print_save_log(f'Showing results from {xtblName}')
    for item in data:
        print(item)


def print_save_log(log_msg):
    """
    Prints the message passed onto it with a timestamp and saves it to a local log file

    :param log_msg: the text that should be saved to the logfile
    :return:
    """
    log_msg = f'{datetime.now().strftime("%m/%d/%Y %H:%M:%S")}: {log_msg}'
    logging.info(log_msg)
    print(log_msg)


def elapsed_time():
    """
    Prints how much time has lapsed during the execution of the script

    :return:
    """

    # Local variables
    time_message = 'Total execution time - '
    seconds_diff = (datetime.now() - start_time).total_seconds()
    days_diff = int(seconds_diff // 86400)
    hours_diff = int(seconds_diff // 3600) % 24
    minutes_diff = int(seconds_diff // 60) % 60

    try:
        if days_diff > 0:
            print_save_log(f'{time_message} {days_diff} day(s) {hours_diff} hour(s) '
                           f'{minutes_diff} minute(s)')
        elif hours_diff > 0:
            print_save_log(f'{time_message} {hours_diff} hour(s) {minutes_diff} minute(s)')
        elif minutes_diff > 0:
            print_save_log(f'{time_message} {minutes_diff} minute(s)')
        else:
            print_save_log(f'{time_message} {int(seconds_diff)} second(s)')
    except Exception as e:
        print_save_log(e)
        pass


if __name__ == "__main__":
    print_save_log('Starting to execute script')

    create()  # Function to create the database and table to be used in this example
    insert()  # Function to insert data into our table. Currently using a python list
    delete()  # Function to delete data in the table

    # Closes the connection to the database
    con.close()

    elapsed_time()
