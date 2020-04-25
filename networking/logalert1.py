#!/usr/bin/env python3

#Test script that runds every 60 seconds and
#checks the length of sshd logs and
#sends out tweet if new activity (record lines) are detected


import time
import os
import subprocess

from twython import Twython

from auth import(
        API_key,
        API_secret_key,
        access_token,
        access_token_secret
)

twitter = Twython(
        API_key,
        API_secret_key,
        access_token,
        access_token_secret
)


check_log = 'grep sshd /var/log/auth.log | wc -l'

grep_string = 'grep sshd /var/log/auth.log | tail -n '

prev_file_len = int(subprocess.check_output(check_log,shell=True))

print(f"log file length: {prev_file_len}")

while True:

        time.sleep(60)

        file_len = int(subprocess.check_output(check_log,shell=True))

        message = (f'log file length: {file_len}')

        print (message)



        if file_len > prev_file_len:

                twitter.update_status(status=message)

                grep_string_new = grep_string + str(file_len-prev_file_len)

                new_logs = subprocess.check_output(grep_string_new,shell=True) 

                print(new_logs.decode('utf-8'))

                prev_file_len = file_len

