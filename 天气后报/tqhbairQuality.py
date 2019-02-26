import urllib.request
from urllib.error import HTTPError
import requests
from bs4 import BeautifulSoup
import csv
import time

cook='bdshare_firstime=1527492825463; Hm_lvt_f48cedd6a69101030e93d4ef60f48fd0=1527492825,1527665282; __51cke__=; ASP.NET_SessionId=d3r5yj55c4frnlzywjdnyx45; Hm_lpvt_f48cedd6a69101030e93d4ef60f48fd0=1527670096; __tins__4560568=%7B%22sid%22%3A%201527670096246%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201527671896246%7D; __51laig__=16'
headers = {
    "Cookie":cook,
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

def getObj(url):
    for i in range(5):
        try:
            html=requests.get(url,headers=headers)
            html.encoding="gbk"
        except HTTPError as e:
            # time.sleep(3)
            print('再次请求')
            print('HTTPError')
        try:
            bsObj = BeautifulSoup(html.text,'lxml')
            obj=bsObj.find('div',class_='api_month_list')
            return obj
        except AttributeError as e:
            print('AttributeError')
            # return None
    return bsObj

def getCity(url):
    f=open('aricity.txt','w+',encoding='utf-8')
    obj=getObj(url).find('div',class_='citychk').find_all('dl')
    direct=obj[0].find('dd').find_all('a')
    for m in range(0,4):
        if 'href' in direct[m].attrs:
            f.write(str([direct[m].get_text(),direct[m].attrs['href']])+'\n')

    for i in range(1,len(obj)):
        dd=obj[i].find('dd').find_all('a')
        for n in range(len(dd)):
            if 'href' in dd[n].attrs:
                f.write(str([dd[n].get_text(),dd[n].attrs['href']])+'\n')

url='http://www.tianqihoubao.com/aqi/'
# getCity(url)


def gethistort():
    ym=[]
    for j in range(2018,2012,-1):
        if j==2018:
            for i in range(5,0,-1):
                if i<10:
                    ym.append(str(j)+'0'+str(i))
            continue
        if j==2013:
            for i in range(12,9,-1):
                ym.append(str(j)+str(i))
            continue
        for i in range(12,0,-1):
            if i<10:
                ym.append(str(j)+'0'+str(i))
            else:
                ym.append(str(j)+str(i))
                


    frcity=open('aricity.txt','r',encoding='utf-8')
    outurl=open('airUrl.txt','w+',encoding='utf-8')
    for row in frcity:
        row=eval(row)
        city=row[1][5:][:-5]
        for i in ym:
            newUrl=url+city+'-'+i+'.html'
            outurl.write(str([row[0],newUrl])+'\n')


    
def getdetail1(row):
    url=row[1]
    trlist=getObj(url).find_all('tr')
    # print(len(trlist))
    for i in range(1,len(trlist)):
        wrow=[row[0]]
        tr=trlist[i]
        tdlist=tr.find_all('td')
        for t in range(0,len(tdlist)):
            wrow.append(tdlist[t].get_text())
        csv_write.writerow(wrow)

fhistory=open('airUrl.txt','r',encoding='utf-8')
finalout=open('finalout.csv','a+',encoding='gb18030',newline='')
fwrong=open('wrong.txt','a+',encoding='gb18030')
csv_write=csv.writer(finalout)
n=0
for row in fhistory:
    if n==0:
        n=1
        continue
    row=eval(row)
    print(row)
    # phangetObj(row)
    for i in range(4):
        try:
            getdetail1(row)
            break
        except:
            continue
        if i==3:
            fwrong.write(str(row)+'\n')
            
            
    # break


# http://www.tianqihoubao.com/aqi/beijing-201805.html
# http://www.tianqihoubao.com/aqi/beijing-201805.html
# view-source:http://www.tianqihoubao.com/aqi/beijing-201805.html
# view-source:http://www.tianqihoubao.com/aqi/beijing-201805.html