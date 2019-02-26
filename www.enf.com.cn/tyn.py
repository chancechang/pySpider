
import requests
import csv
import time
import json
import re
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
# f1=open('link.txt','a+',encoding='utf-8')
# for i in range(1,3)
# url='https://www.enf.com.cn/directory/installer/Portugal?page=2'
# bsObj=mytemp.getObj(url,True)
# table=bsObj.find('table',class_='enf-list-table ').find_all('tr')
# for tr in table:
#     link=tr.find('a').attrs['href']
#     print(link)
#     f1.write(link+'\n')
# print(table)
f2=open('Portugal.csv','w+',encoding='gb18030',newline='')
csv_write=csv.writer(f2)

def getDetail(url):
    url='https://www.enf.com.cn'+url
    print(url)
    bsObj=mytemp.getObj(url,True)
    div=bsObj.find('div',class_='enf-company-profile-info-main pull-left')
    h1=div.find('h1',class_='blue-title').get_text().replace('\n','').strip()
    try:
        email=div.find('td',itemprop='email').find('a').get_text()
    except:
        email=''
    href=div.find('a',itemprop='url').attrs['title']
    tablelist=div.find('div',class_='enf-company-profile-info-main-spec position-relative').find_all('table')
    l=len(tablelist)
    address=tablelist[l-1].find_all('td')[1].get_text()
    row=[url,h1,email,href,address]
    csv_write.writerow(row)
    print(row)

for line in open('link.txt'):
    getDetail(line)
    # print(line)
# url='/directory/installer/93425/visotela?utm_source=ENF&utm_medium=Portugal&utm_content=93425&utm_campaign=profiles_installer'
# getDetail(url)