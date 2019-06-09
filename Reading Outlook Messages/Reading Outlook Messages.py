# -*- coding: utf-8 -*-
"""
    purpose: To read through an outlook email and parse information.
    author: Alberto Rodriguez
    date: 2019+06+9
"""

import os
import pandas as pd
import win32com.client
from datetime import datetime


# Global Variables
startTime = datetime.now()
date = datetime.now().strftime('%Y+%m+%d')
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Sets to save the file in the directory the script is run


def print_msg(msg):
    # TODO: Save the log message into a text file; Add the time the script is run into the name
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {msg}')


def print_exception(exception):
    print_msg(exception)
    exit(1)


def read_outlook():
    """

    :return: a list that contains the response from the HTTP GET call
    """

    file_path = r'E:\Python Code\Reading Outlook Messages\Messages'
    fileName = 'parsed_outlook_messages.xlsx'

    error_file = []
    emailbody = []

    for root, dirs, files in os.walk(file_path):
        for outlook_file in files:
            outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
            try:
                # Will try to open the outlook file
                print_msg(f'Attemping to read "{outlook_file}"')
                msg = outlook.OpenSharedItem(f'{file_path}\{outlook_file}')

                # Store the full email body to be exported later
                emailbody.append({
                    'fileName': outlook_file,
                    'emailBody': msg.body
                })


            except Exception as e:
                print_exception(e)
                error_file.append(outlook_file)

    # Declare the Excel writer object to write multiple sheets
    with pd.ExcelWriter(fileName) as writer:
        pd.DataFrame(emailbody).to_excel(writer, index=False, sheet_name='parsed_full_email_body',
                                         columns=['fileName', 'emailBody'])

        pd.DataFrame(error_file).to_excel(writer, index=False, sheet_name='errors_with_files')


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


if __name__ == '__main__':
    read_outlook()
    elapsed_time()
