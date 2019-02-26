from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
import time
import json

url='https://gz.17zwd.com/api/shop/get-list/73'
resp=requests.get(url)
f=open('17wang.txt','w+',encoding='utf-8')
f.write(resp.text)
print(resp.text)