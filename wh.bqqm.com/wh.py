
from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp

#武汉便民网信用卡

# f1=open('wh_xyk_link.csv','w+',encoding='gb18030',newline='')
# csv_write1=csv.writer(f1)

# for i in range(1,21):
#     url='http://wh.bqqm.com/xinyongka/p'+str(i)
#     bsObj=mytemp.getObj(url)
#     trlist=bsObj.find('table',class_='tbimg1').find_all('tr')
#     for tr in trlist:
#         a=tr.find('div',class_='tblist_t').find('a')
#         title=a.get_text()
#         href=a.attrs['href']
#         row=[title,href]
#         print(row)
#         csv_write1.writerow(row)


def get_detail():
    f2=open('wh_xyk_final.csv','w+',encoding='gb18030',newline='')
    csv_write2=csv.writer(f2)
    for line in csv.reader(open('wh_xyk_link.csv','r',encoding='gb18030')):  
        url='http://wh.bqqm.com'+line[1]
        bsObj=mytemp.getObj(url)
        phone=bsObj.find('div',class_='telli').find('span',class_='p').get_text()
        row=[line[0],url,phone]
        print(row)
        csv_write2.writerow(row)
get_detail()