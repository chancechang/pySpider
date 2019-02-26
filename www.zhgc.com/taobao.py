
from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
url='https://s.taobao.com/search?q=%E8%8C%B6%E5%8F%B6&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.2&ie=utf8&initiative_id=tbindexz_20170306&cps=yes&ppath=122216450%3A30419'
