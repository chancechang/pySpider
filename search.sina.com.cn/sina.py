from decimal import Decimal
from bs4 import BeautifulSoup
import requests
import time
import datetime
import json
import re
import xlsxwriter
import xlrd
def get_proxies_abuyun():
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"
    # 代理隧道验证信息
    proxyUser = 'HR3LY43V4QOU249D'
    proxyPass = 'F89DAEA7A6C85E23'

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies
cook='SINAGLOBAL=111.175.187.177_1501208803.914805; U_TRS1=000000c8.b5f67cdc.59a1611b.b5c2d9f5; SUB=_2AkMssHxdf8NxqwJRmPATzGnnaYRwzwnEieKa7I2GJRMyHRl-yD9jqmA6tRB6BzBSssCQGiaUBzsW5FpTk-BW0y_EF2Ie; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5kqUa2MwHrFB1UIrO4ZSQA; U_TRS2=00000054.7d4a69ec.5c1f2c30.3be3779f; WEB2_OTHER=5933568c53e5c7bf18f26e1b08f30a6d; UOR=,search.sina.com.cn,; Apache=218.197.238.84_1545546826.782959; ULV=1545546834984:2:2:2:218.197.238.84_1545546826.782959:1545546831696; lxlrttp=1545098194'
cook='SINAGLOBAL=111.175.187.177_1501208803.914805; U_TRS1=000000c8.b5f67cdc.59a1611b.b5c2d9f5; SUB=_2AkMssHxdf8NxqwJRmPATzGnnaYRwzwnEieKa7I2GJRMyHRl-yD9jqmA6tRB6BzBSssCQGiaUBzsW5FpTk-BW0y_EF2Ie; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5kqUa2MwHrFB1UIrO4ZSQA; U_TRS2=00000054.7d4a69ec.5c1f2c30.3be3779f; UOR=,search.sina.com.cn,; Apache=218.197.238.84_1545546826.782959; ULV=1545546834984:2:2:2:218.197.238.84_1545546826.782959:1545546831696; CNZZDATA5399792=cnzz_eid%3D720668383-1545544528-http%253A%252F%252Ffinance.sina.com.cn%252F%26ntime%3D1545544528; CNZZDATA5661630=cnzz_eid%3D18623419-1545544461-http%253A%252F%252Ffinance.sina.com.cn%252F%26ntime%3D1545544461; lxlrttp=1545098194; CNZZDATA1260051864=46509534-1545542984-null%7C1545544670; CNZZDATA5581086=cnzz_eid%3D564302732-1545543163-null%26ntime%3D1545547466'
header={
    # 'Cookie':cook,
    # 'Host':'news.sina.com.cn',
    # 'Referer':'http://search.sina.com.cn/?c=news&q=%CD%F8%D4%BC%B3%B5&range=title&time=custom&stime=2017-09-01&etime=2018-08-31&num=20&col=&source=&from=&country=&size=&a=&page=48&pf=2132736211&ps=2132736864&dpc=1',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
}

def get_link():
    f=open('sina.txt','a+',newline='',encoding='utf-8')
    for i in range(200,300):
        print(i)
        url='http://search.sina.com.cn/?c=news&q=%CD%F8%D4%BC%B3%B5&range=title&time=custom&stime=2017-09-01&etime=2018-08-31&num=20&page='+str(i)
        # url='http://search.sina.com.cn/?c=news&q=%CD%F8%D4%BC%B3%B5&range=title&time=custom&stime=2017-09-01&etime=2018-08-31&num=20&col=&source=&from=&country=&size=&a=&page=46&pf=2132736211&ps=2132736864&dpc=1'
        # url='http://search.sina.com.cn/?c=news&q=%CD%F8%D4%BC%B3%B5&range=title&time=custom&stime=2017-09-01&etime=2018-08-31&num=20&col=&source=&from=&country=&size=&a=&page=11&pf=2131425455&ps=2134309112&dpc=1'
        req=requests.get(url,headers=header)
        bsObj=BeautifulSoup(req.text,'html.parser')
        divlist=bsObj.find('div',{'id':'result'}).find_all('div',class_='r-info r-info2')
        print(len(divlist))
        for div in divlist:
            a=div.find('a')
            href=a.attrs['href']
            title=a.get_text()
            fgray_time=div.find('span',class_='fgray_time').get_text()
            name=fgray_time.split(' ')[0]
            time=fgray_time.replace(name,'').strip()
            row=[href,title,name,time]
            f.write(str(row)+'\n')
        print(row)  
        # break   
    f.close()
# get_link()

def get_detail():
    r=0
    f=open('sina_error2.txt','a+',newline='',encoding='utf-8')
    f1=open('sina_detail.txt','a+',newline='',encoding='utf-8')
        

    for line in open('sina_error1.txt','r',encoding='utf-8'):
        print(r)
        row=eval(line)
        print(row[0])
        header['Host']=row[0].split('/')[2]

        req=requests.get(row[0],headers=header,timeout=15)
        req.encoding='utf-8'
        bsObj=BeautifulSoup(req.text,'html.parser')
        print(bsObj)
        try:
            text=bsObj.find('div',class_='article').get_text()
        except:
            f.write(str(row)+'\n')
            continue    
        row.append(text)
        print(text[:100])
        f1.write(str(row)+'\n')

        r=r+1
        # break
    # workbook.close()
    f.close()
    f1.close()

workbook = xlsxwriter.Workbook('sina_网约车.xlsx')     #创建工作簿
sheet = workbook.add_worksheet()
r=0
for line in open('sina_detail.txt','r',encoding='utf-8'):
    row=eval(line)
    for i in range(len(row)):
        sheet.write(r,i,row[i])
    r=r+1
workbook.close()