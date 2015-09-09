#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Install BS4 with pip3 : sudo pip3 install -U beautifulsoup4
from bs4 import BeautifulSoup
# Install Requests with pip3 : sudo pip3 install -U requests
import urllib.request as urllib2

# Define URL for data scraping
checkurl = 'http://pocasie.sme.sk/krajina/slovensko/bratislava/'
# Open URL in URLlib
checkpage = urllib2.urlopen(checkurl)
# Read and parse html data
checksoup = BeautifulSoup(checkpage.read(), "html.parser")

# Get values with BS
temp_current_val = checksoup.find_all('span', 'pocasie-current-box-now-temp')[0].text.split('°')[0]
temp_today_max = checksoup.find_all('span', 'pocasie-current-box-minmax-max')[0].text.split()[2]
temp_today_min = checksoup.find_all('span', 'pocasie-current-box-minmax-min')[0].text.split()[2]

# Print values
print("Aktualna Teplota: ", temp_current_val)
print("Dnesne Maximum: ", temp_today_max)
print("Dnesne Minimum: ", temp_today_min)
# Another method how to parse data
temp_today_alternative = checksoup.find_all('b')[1].text.replace('°C', '')
print("\nAlternative temp: ", temp_today_alternative)
