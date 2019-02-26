#http://guba.eastmoney.com/list,601198,f_1.html

from bs4 import BeautifulSoup
import requests
import csv
from requests.adapters import HTTPAdapter

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=10))
s.mount('https://', HTTPAdapter(max_retries=10))

root='http://guba.eastmoney.com/'
root1='list,601198,f_'
out=open('dfcf.csv', 'w+',encoding='gb18030',newline = '')
csv_write=csv.writer(out)
csv_write.writerow(['阅读量','评论量','标题','作者','发布日期'])
publishPerDay={}
def crawl(pagenum,sum):
    if pagenum>sum:
        return
    req=s.get(root+root1+str(pagenum)+'.html',timeout=100)
    req.encoding='utf-8'
    soup=BeautifulSoup(req.text,'html.parser')
    articallist=soup.find_all('div',class_='articleh')
    # print(len(articallist))
    for i in range(0,len(articallist)):
        if len(articallist[i].find_all('span'))<3:
            continue
        if articallist[i].find('em'):
            if articallist[i].find('em').string=='大赛':
                continue
        readNum=articallist[i].find('span',class_='l1').string
        commentNum=articallist[i].find('span',class_='l2').string
        title=articallist[i].find('span',class_='l3').find_all('a')[-1].string
        url=articallist[i].find('span',class_='l3').find_all('a')[-1]['href'].replace('/','')
        author=articallist[i].find('span',class_='l4').a.string
        
        # print(root+url)
        req1=s.get(root+url,timeout=100)
        req1.encoding='utf-8'
        soup1=BeautifulSoup(req1.text,'html.parser')
        # print(soup1.find('div',class_='zwfbtime'))
        if soup1.find('div',class_='zwfbtime')==None:
            continue
        publishTime=soup1.find('div',class_='zwfbtime').string.split(' ')[1]        
        publishPerDay.setdefault(publishTime,0)
        publishPerDay[publishTime]=publishPerDay[publishTime]+1
        print(readNum,commentNum,title,author,publishTime)
        csv_write.writerow([readNum,commentNum,title,author,publishTime])
    pagenum=pagenum+1
    return crawl(pagenum,sum)


crawl(1,87)
print(publishPerDay)