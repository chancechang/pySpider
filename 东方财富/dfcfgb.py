#http://guba.eastmoney.com/list,zssh000001_1.html

from bs4 import BeautifulSoup
import requests
import csv
import threading
# from log import info_logger


def build_request(url):
    for i in range(5):
        try:
            req=requests.get(url,timeout=20)
            return req
        except:
            continue
    return None

root='http://guba.eastmoney.com/'
root1='list,zssh000001_'
out=open('dfcfgbtest.csv', 'w+',encoding='gb18030',newline = '')
csv_write=csv.writer(out)
csv_write.writerow(['评论数','阅读数','时间','标题','内容'])


def crawl(pagenum,sum):
    if pagenum>sum:
        return
    req=build_request(root+root1+str(pagenum)+'.html')
    req.encoding='utf-8'
    soup=BeautifulSoup(req.text,'html.parser')
    articallist=soup.find_all('div',class_='articleh')
    # print(len(articallist))
    # if len(articallist)<80:
    #     print('重新爬取第'+str(pagenum)+'页')
    #     print('网址：'+root+root1+str(pagenum)+'.html')
    #     return crawl(pagenum,sum)
    for i in range(0,len(articallist)):
        if len(articallist[i].find_all('span'))<3:
            # print(articallist[i])
            continue
        readNum=articallist[i].find('span',class_='l1').string
        commentNum=articallist[i].find('span',class_='l2').string
        title=articallist[i].find('span',class_='l3').find_all('a')[-1].string
        url=articallist[i].find('span',class_='l3').find_all('a')[-1]['href'].replace('/','')
               
        # print(root+url)
        req1=build_request(root+url)
        req1.encoding='utf-8'
        soup1=BeautifulSoup(req1.text,'html.parser')
        # print(soup1.find('div',class_='zwfbtime'))
        if soup1.find('div',class_='zwfbtime')==None:
            continue
        publishTime=soup1.find('div',class_='zwfbtime').string.split(' ')[1]        
        if publishTime.find('2017')==0:
            if soup1.find('div',{'id':'zw_body'}):
                content=soup1.find('div',{'id':'zw_body'}).get_text()       
            else:
                content=soup1.find('div',class_='stockcodec').get_text()
            if publishTime.find('2017')==0:
                print(commentNum,readNum,publishTime,title)
                csv_write.writerow([commentNum,readNum,publishTime,title,content])
    pagenum=pagenum+1
    print('即将开始爬取第'+str(pagenum)+'页')
    return crawl(pagenum,sum)


crawl(50,6899)

