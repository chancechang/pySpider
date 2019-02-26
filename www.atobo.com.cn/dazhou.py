from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
import time



cook='Hm_lvt_88ac9d6018876c5ce132e00a6b66ef09=1538654073; Hm_lpvt_88ac9d6018876c5ce132e00a6b66ef09=1538654188'

def get_link():
    f1=open('company_link.csv','w+',encoding='gb18030',newline='')
    csv_write=csv.writer(f1)
    for i in range(1,51):
        if i==1:
            url='https://www.atobo.com.cn/Companys/s-p26-s579/'
        else:
            url='https://www.atobo.com.cn/Companys/s-p26-s579-y'+str(i)+'/'

        bsObj=mytemp.getObj(url,False,cook)   
        lilist=bsObj.find('div',class_='product_contextlist bplist').find_all('li',class_='product_box')
        for li in lilist:
            attrS=li.find('li',class_='pp_name').find('a').attrs
            title=attrS['title']
            link=attrS['href']
            row=[title,link]
            print(row)
            csv_write.writerow(row)


f2=open('company_final.csv','a+',encoding='gb18030',newline='')
csv_write2=csv.writer(f2)
f3=open('company_error1.csv','w+',encoding='gb18030',newline='')
csv_write3=csv.writer(f3)
for line in csv.reader(open('company_error.csv','r',encoding='gb18030')):  
    url=line[1]
    print(url)
    bsObj=mytemp.getObj(url,True,cook).find('div',class_='card-context')
    try:
        ullist=bsObj.find_all('ul')
    except:
        time.sleep(2)
        bsObj=mytemp.getObj(url,True,cook).find('div',class_='card-context')
        try:
            ullist=bsObj.find_all('ul')
        except:
            csv_write3.writerow(line)
            continue
    name=''
    tele=''
    for ul in ullist:
        text=ul.get_text()
        if '联系' in text:
            name=ul.find('li',class_='card-right').get_text()
            continue
        if '电话' in text:
            tele=ul.find('li',class_='card-right').get_text()+'\t'
            continue
        if '手机' in text:
            tele=ul.find('li',class_='card-right').get_text()+'\t'
    row=line+[name,tele]
    print(row)
    csv_write2.writerow(row)
        



   