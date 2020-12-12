import urllib.request
from bs4 import BeautifulSoup
import json
from urllib import parse
from collections import OrderedDict
from datetime import datetime

basic_url = "https://finance.naver.com/sise/"
fp = urllib.request.urlopen(basic_url)
source = fp.read()
fp.close()

soup = BeautifulSoup(source, 'html.parser')
soup = soup.findAll("span", class_="num")
kospi_value = soup[0].string

# json 형식으로 만들기

stock_data = OrderedDict()

stock_data['kospi'] = kospi_value

print(stock_data)

{
    "kospi": "현재 코스피가"
}