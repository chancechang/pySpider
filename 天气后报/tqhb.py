import urllib.request
from urllib.error import HTTPError
import requests
from bs4 import BeautifulSoup
import csv
import time

cook='Hm_lvt_f48cedd6a69101030e93d4ef60f48fd0=1527492825; __51cke__=; bdshare_firstime=1527492825463; ASP.NET_SessionId=jqh53x2xqur3jx45e3oxog45; Hm_lpvt_f48cedd6a69101030e93d4ef60f48fd0=1527492986; __tins__4560568=%7B%22sid%22%3A%201527492824619%2C%20%22vd%22%3A%206%2C%20%22expires%22%3A%201527494786067%7D; __51laig__=6'
headers = {
    "Cookie":cook,
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

def getObj(url):
    for i in range(5):
        try:
            html=requests.get(url,headers=headers)
            html.encoding="gbk"
            break
        except HTTPError as e:
            # time.sleep(3)
            print('再次请求')
            print('HTTPError')
            return None
    try:
        bsObj = BeautifulSoup(html.text,'html.parser')
    except AttributeError as e:
        print('AttributeError')
        return None
    return bsObj

def getProvince(url):
    fp=open('province.txt','w+',encoding='gb18030')
    trlist=getObj(url).find('div',{'id':'content'}).find_all('table')[1].find_all('tr')
    for tr in trlist:        
        tdlist=tr.find_all('td')
        for td in tdlist:
            a=td.find('a')
            row=[a.get_text(),a.attrs['href']]
            # print(row)
            fp.write(str(row)+'\n')


url='http://www.tianqihoubao.com/'
# getProvince(url)

def getcity(line):
    newurl=url+line[1]
    city=line[0]

    trlist=getObj(newurl).find('div',{'id':'content'}).find_all('table')[0].find_all('tr')
    for tr in trlist:        
        tdlist=tr.find_all('td')
        for td in tdlist:
            a=td.find('a')
            row=[city,a.get_text(),a.attrs['href']]
            print(row)
            fcity.write(str(row)+'\n')


# fcity=open('city.txt','w+',encoding='utf-8')    
# for line in open('province.txt','r'):
#     line=eval(line)
#     getcity(line)

def getdetail(line):
    newurl=url+'lishi'+line[2][3:]
    print('即将抓取'+newurl)
    divlist=getObj(newurl).find('div',{'id':'content'}).find_all('div',class_='box pcity')
    if len(divlist)!=8:
        print('waring')
    for div in divlist:
        ullist=div.find_all('ul')
        for ul in ullist:
            lilist=ul.find_all('li')
            for i in range(1,len(lilist)):
                if 'href' in lilist[i].find('a').attrs:                
                    a=lilist[i].find('a').attrs['href']
                    if a[0]!='/':
                        a='/lishi/'+a
                    # print(a)
                    row=line[:2]+[a[-11:-5],url+a[1:]]
                    # print(row)
                    csv_write.writerow(row)

# out=open('tianqifinal.csv','a+',encoding='gb18030',newline='') 
# csv_write=csv.writer(out)
# t=0
# for line in open('city.txt','r',encoding='utf-8'):
#     if t==0:
#         t=1
#         continue
    
#     print(line)
#     line=eval(line)
#     getdetail(line)
    
    
  



