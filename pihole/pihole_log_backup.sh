#!/bin/bash

#sample_log=$(zcat /var/log/pihole.log.2.gz | head -n 500 | tail -n 1)
 
date_log=$(stat -c '%y' /var/log/pihole.log.2.gz | cut -d ' ' -f1 | sed -e 's/-//g')

date_delta=1

date_yest=$(date --date="${date_log} -${date_delta} day" +%Y%my%d)

filename="pihole.log.${date_yest}.gz"

echo $filename

cp /var/log/pihole.log.2.gz ~/archive/test.gz
