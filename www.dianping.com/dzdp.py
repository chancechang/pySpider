
import urllib.request 
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import requests
import csv
import json
import time

cook='_lxsdk_cuid=162b866f068f-0113aab1e382e6-b353461-100200-162b866f069c8; _lxsdk=162b866f068f-0113aab1e382e6-b353461-100200-162b866f069c8; _hc.v=4c8fc833-5973-1e1e-f675-a4fbfb2fa6e9.1523512181; _lxsdk_s=162b866f09b-f29-2da-841%7C%7C1244'
headers = {
    "Cookie":cook,
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept - Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Host':'www.dianping.com',
    'Connection':'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    }

def getObj(url):
    for i in range(3):
        try:
            html=requests.get(url,headers=headers)
            html.encoding="utf-8"
        except HTTPError as e:
            print('HTTPError')
        try:
            print(html)
            bsObj = BeautifulSoup(html.text,'html.parser')
            return bsObj
        except AttributeError as e:
            print('AttributeError')
    return None        
    
def crawl(url,csv_write):
    # data=getJson(url)
    # print(data[0])
    bsObj=getObj(url).find('div',class_='reviews-items')
    lilist=bsObj.find('div',class_='main-review')
    print(len(lilist))
    for li in lilist:
        try:
            text=li.find('div',class_='review-words').get_text().replace('收起评论','').strip()
            time=li.find('div',class_='misc-info').find('span',class_='time').get_text().strip().split(' ')[0]
            scoreClass=li.find('span',class_='sml-rank-stars').attrs['class']
            for cla in scoreClass:
                if cla.find('sml-str')==0:
                    score=int(cla[7:9])
            print(text,time,score)
            csv_write.writerow([text,time,score])
        except:
            print(li)
 
        

#csv文件的读取
urlroot1='http://www.dianping.com/shop/58839368/review_all/p'

out=open('dzdp.csv', 'w+',encoding='gb18030',newline = '')
csv_write=csv.writer(out)
for i in range(1,708):
    newUrl=urlroot1+str(i)
    print('即将爬取'+newUrl)
    crawl(newUrl,csv_write)
    time.sleep(10)
    
