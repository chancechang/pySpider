
from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
import time

data={
    'wid':'346171123114509',
    'dateGroup':'9month'
}
header={
    'Referer':'http://data.weibo.com/index/newindex?visit_type=trend&wid=346171123114509',
    'User-Agent':'Android'
}
url='http://data.weibo.com/index/ajax/newindex/getchartdata'
req=requests.post(url,data,headers=header)
print(req.text)