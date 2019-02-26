from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
import time


url='http://www.zhgc.com/mk/ss.asp?zl=a'
data={
    'pxfs':4,
    'jls':10,
    'bzzs':'',
    'jumpPage':7060,
    'newpage':'',
}
header={
    'Cookie':'ASPSESSIONIDASATQCTQ=NINILHBCCLGBLAPFEHMJNBME; ASPSESSIONIDCSDQQBQT=CIDPHBDCEOGLALALPMNBAAKP; upNum=0'
}
html=requests.post(url,data=data,headers=header)
html.encoding='gb2312'
bsObj=BeautifulSoup(html.text,'html.parser')
table=bsObj.find('table',{'id':'AutoNumber1'})
trlist=table.find_all('tr')
for tr in trlist:
    print(tr.get_text())
