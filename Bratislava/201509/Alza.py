#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Install BS4 with pip3 : sudo pip3 install -U beautifulsoup4
from bs4 import BeautifulSoup
# Install Requests with pip3 : sudo pip3 install -U requests
import urllib.request as urllib2

# Define URL for data scraping
checkurl = "https://www.alza.sk/macbook-pro-13-retina-cz-2015-d2412494.htm"
# Open URL in URLlib
checkpage = urllib2.urlopen(checkurl)
# Read and parse html data
checksoup = BeautifulSoup(checkpage.read(), "html.parser")

# Get values with BS
tovar_nazov = checksoup.find_all('h1')[0].text.replace("\n", "").replace("\r", "")
tovar_popis = checksoup.find('div', class_='nameextc').text.replace("\n", "")
tovar_cena = checksoup.find('span', class_='price_withVat').text.replace("\xa0", "")

# Print values
print("URL:", checkurl)
print("Názov:", tovar_nazov)
print("Popis:", tovar_popis)
print("Cena:", tovar_cena)


# print("\n##### DEBUG ####")
# print(str(checksoup.find_all('h1')[0].text).encode('utf-8'))
# file_out = open("text.html", "w")
# file_out.write(str(tovar_cena.encode("utf-8")))
