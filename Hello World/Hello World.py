# -*- coding: utf-8 -*-
"""
Created on Sat May 19 13:17:07 2018

@author: Rodri_000
"""

import os
import logging
from datetime import datetime


# Global Variables
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Sets working directory to folder the script is being run from
logging.basicConfig(filename='Hello World Log.log', level=logging.DEBUG)  # The name of the log file
start_time = datetime.now()


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
    print_save_log('Hello World')
    elapsed_time()
