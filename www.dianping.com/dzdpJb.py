from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
import time


urlroot1 = 'http://www.dianping.com/shanghai/ch30/g133p'
urlroot2 = '?aid=93371072%2C23727607%2C69852302%2C57529888&cpt=93371072%2C23727607%2C69852302%2C57529888'

# cook='_lxsdk_cuid=162b866f068f-0113aab1e382e6-b353461-100200-162b866f069c8; _lxsdk=162b866f068f-0113aab1e382e6-b353461-100200-162b866f069c8; _hc.v=4c8fc833-5973-1e1e-f675-a4fbfb2fa6e9.1523512181; cy=1; cye=shanghai; s_ViewType=10; cityid=1; default_ab=shop%3AA%3A1%7CshopList%3AA%3A1; _lxsdk_s=1664e103504-bf6-1c3-704%7C%7C106'
cook='_lxsdk_cuid=162b866f068f-0113aab1e382e6-b353461-100200-162b866f069c8; _lxsdk=162b866f068f-0113aab1e382e6-b353461-100200-162b866f069c8; _hc.v=4c8fc833-5973-1e1e-f675-a4fbfb2fa6e9.1523512181; cy=1; cye=shanghai; s_ViewType=10; cityid=1; logan_custom_report=; default_ab=shop%3AA%3A1%7CshopList%3AA%3A1; msource=default; logan_session_token=32izrvlwi560izy0xla8; _lxsdk_s=1664e103504-bf6-1c3-704%7C%7C218'
# cook='_lxsdk_cuid=162b866f068f-0113aab1e382e6-b353461-100200-162b866f069c8; _lxsdk=162b866f068f-0113aab1e382e6-b353461-100200-162b866f069c8; _hc.v=4c8fc833-5973-1e1e-f675-a4fbfb2fa6e9.1523512181; cy=1; cye=shanghai; s_ViewType=10; cityid=1; logan_custom_report=; default_ab=shop%3AA%3A1%7CshopList%3AA%3A1; msource=default; logan_session_token=32izrvlwi560izy0xla8; _lxsdk_s=1664e103504-bf6-1c3-704%7C%7C274'
# cook='_lxsdk_cuid=162b866f068f-0113aab1e382e6-b353461-100200-162b866f069c8; _lxsdk=162b866f068f-0113aab1e382e6-b353461-100200-162b866f069c8; _hc.v=4c8fc833-5973-1e1e-f675-a4fbfb2fa6e9.1523512181; cy=1; cye=shanghai; s_ViewType=10; cityid=1; m_flash2=1; msource=default; default_ab=shop%3AA%3A1%7Cindex%3AA%3A1%7CshopList%3AA%3A1; pvhistory=6L+U5ZuePjo8L2Vycm9yL2Vycm9yX3BhZ2U+OjwxNTM4OTU5NjQyOTYzXV9b; chwlsource=default; logan_custom_report=; switchcityflashtoast=1; logan_session_token=lqwff0khxg2m6nr722sj; _lxsdk_s=1665123fbd8-faf-747-9af%7C%7C96'
def get_link():
    f1=open('dzdp_wedding.csv','w+',encoding='gb18030',newline='')
    csv_write1=csv.writer(f1)
    for i in range(1, 51):
        url = urlroot1 + str(i) + urlroot2
        bsObj=mytemp.getObj(url,False,cook)
        lilist=bsObj.find_all('div',class_='txt')
        print(len(lilist))
        for li in lilist:
            a=li.find('div',class_='tit').find('a')
            href=a.attrs['href']
            title=a.find('h4').get_text()
            row=[title,href]
            print(row)
            csv_write1.writerow(row)
# get_link()

def get_detail():
    
    f2=open('wedding_final.csv','a+',encoding='gb18030',newline='')
    csv_write2=csv.writer(f2)
    f3=open('wedding_error1.csv','w+',encoding='gb18030',newline='')
    csv_write3=csv.writer(f3)
    for line in open('wedding_error.csv','r',encoding='gb18030'):
        
        line=line.split(',')
        if line[0][0]=='"':
            continue       
        # print(line)
        url=str('https://m'+line[1][11:]).strip().replace('\n','')
        print(url)
        # time.sleep(3)
        bsObj=mytemp.getObj(url,False,cook)
        # print(bsObj)
        # print(bsObj.find('body',class_='shop-details'))
        # jo=bsObj.find('textarea',{'id':'shop-detail'}).get_text()
        # print(jo)
        # break
        try:
            address=bsObj.find('div',class_='J_address').get_text().strip()
            phone=bsObj.find('div',class_='J_phone').get_text().strip().replace(' ','')+'\t'
            # print('daoda')
        except:
            csv_write3.writerow(line)
            print(line)
            continue
        row=line+[address,phone]
        print(row)
        csv_write2.writerow(row)
get_detail()