from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp

url='http://www.jiangshi.org/search/kw_NULL_order_1_costmin_0_costmax_0_area_0_page_1.html'

mytemp.getObj(url,)