#https://www.wunderground.com/history/airport/ZHHH/2014/05/01/DailyHistory.html

from bs4 import BeautifulSoup
import requests
import csv
import datetime

def build_request(url):
    for i in range(5):
        try:
            req=requests.get(url,timeout=20)
            return req
        except:
            continue
    return None

root1='https://www.wunderground.com/history/airport/ZHHH/'
root2='/DailyHistory.html'
initialTime=datetime.date(2014,5,1)
endTime=datetime.date(2017,12,31)

def crawl(time):
    t=time.strftime('%Y-%m-%d').replace('-','/')
    req=build_request(root1+t+root2)
    req.encoding='utf-8'
    soup=BeautifulSoup(req.text,'html.parser') 
    div=soup.find('div',class_='large-12')   
    trlist=div.tbody.find_all('tr')
    for tr in trlist:
        
        if tr
            i=i+2
            continue
        
        i=i+2


t=datetime.date(2014,5,1).strftime('%Y-%m-%d').replace('-','/')


def numTwo