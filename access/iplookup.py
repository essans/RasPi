#!/usr/bin/env python3

from pprint import pprint
from ipwhois import IPWhois

ip_addr = '172.247.84.3'

obj = IPWhois(ip_addr)

res = obj.lookup_whois()

src_name = res['nets'][0]['name']
src_descr = res['nets'][0]['description']
src_cntry = res['nets'][0]['country']
src_city = res['nets'][0]['city']
src_state = res['nets'][0]['state']
src_addr = res['nets'][0]['address'].replace('\n',',')
src_emails = str(res['nets'][0]['emails'])

