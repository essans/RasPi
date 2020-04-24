#!/bin/bash

HOST='raspi.soobratty.com'
USER=''
PASSWORD=''

cd /home/pi/log

ftp -inv $HOST <<EOF
user $USER $PASSWORD

mput *.log

bye
