#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Install BS4 with pip3 : sudo pip3 install -U beautifulsoup4
from bs4 import BeautifulSoup
# Install Requests with pip3 : sudo pip3 install -U requests
import urllib.request as urllib2

# Starting URL ID
urlid = 8000
# Ending URL ID
end_urlid = urlid + 5000

# Iterate through URL ID and scrape data
while urlid <= end_urlid:
    # Define URL for data scraping
    checkurl = ("http://www.orsr.sk/vypis.asp?ID=" + str(urlid) + "&SID=3")
    # Open URL in URLlib
    checkpage = urllib2.urlopen(checkurl)
    # Read and parse html data
    checksoup = BeautifulSoup(checkpage.read(), "html.parser")
    print("\n###############\nURL :", checkurl)

    try:
        # Get values with BS
        obch_meno = checksoup.find_all('td')[11].find('span').text[2:]
        sidlo_1 = checksoup.find_all('td')[15].find_all('span')[0].text[2:]
        sidlo_2 = checksoup.find_all('td')[15].find_all('span')[1].text[2:]
        sidlo_3 = checksoup.find_all('td')[15].find_all('span')[2].text[2:]
        sidlo_4 = checksoup.find_all('td')[15].find_all('span')[3].text[2:].replace(" ", "")
        ico = checksoup.find_all('td')[19].find('span').text[2:].replace(" ", "")

        # Print values
        print(obch_meno)
        print(ico)
        # print(sidlo_1)
        # print(sidlo_2)
        # print(sidlo_3)
        # print(sidlo_4)
        print(sidlo_1, sidlo_2, sidlo_3, sidlo_4)

    except:
        print("Neplatne ID")

    urlid = urlid + 1
