import requests
import re
from bs4 import BeautifulSoup
import time
import xlsxwriter
import json
import random
import sys
sys.path.append("..")
import mytemp
cook='__jsluid=7cf08b57822718cf3a6e8d55aeecfcf4; g=75385_1541067918668; CNZZDATA-FE=CNZZDATA-FE; _ga=GA1.2.1624860476.1541067919; _gid=GA1.2.114635946.1541067919; Hm_lvt_dfa5478034171cc641b1639b2a5b717d=1541067920; UM_distinctid=166cece51581e6-0528a7cca96e2-b353461-100200-166cece515a98; CNZZDATA1256706712=954015385-1541065332-https%253A%252F%252Fwww.google.com%252F%7C1541065332; _gat=1; Hm_lpvt_dfa5478034171cc641b1639b2a5b717d=1541068198'
header={
    'Cookie':cook,
#     Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
# Accept-Encoding:gzip, deflate, br
# Accept-Language:zh-CN,zh;q=0.9
# Cache-Control:max-age=0
# Connection:keep-alive
    'Host':'www.haodf.com',
    'Referer':'https://www.haodf.com/',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}
# f1=open('科室link.txt','w+',encoding='utf-8')
# url='https://www.haodf.com/hospital/DE4raCNSz6Om-9cfC2nM4CIa.htm'
# bsObj=requests.get(url,headers=header)
# bsObj=BeautifulSoup(bsObj.text,'html.parser')
# li=bsObj.find('ul',class_='faculty-list').find_all('div',class_='f-l-i-s-i-wrap')
# for l in li:
#     href=l.find('a').attrs['href']
#     title=l.find('a').get_text()
#     f1.write(str([title,href])+'\n')

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
def getDoctorLink():
    f2=open('医生link.txt','w+',encoding='utf-8')
    for line in open('科室link.txt','r',encoding='utf-8'):
        line=eval(line)
        id=re.search(r'faculty\/(.+?).htm',line[1]).group(1)
        i=1
        while True:
            url='https://www.haodf.com/faculty/'+id+'/menzhen_'+str(i)+'.htm'
            print(url)
            for t in range(5):
                try:
                    bsObj=requests.get(url,headers=header,proxies=get_proxies_abuyun(),  timeout=15)
                    break
                except Exception as e:
                    if '429' in str(e):
                        time.sleep(random.randint(0, 1000)/1000.0)
                    continue
            bsObj=BeautifulSoup(bsObj.text,'html.parser')

            table=bsObj.find('table',{'id':'doc_list_index'}).find_all('tr')
            if len(table)==0:
                break
            print(len(table))
            for tr in table:
                a=tr.find('a',class_='name').attrs
                title=a['title']
                href=a['href']
                row=[title,href]
                f2.write(str(row)+'\n')
            i=i+1
            # time.sleep(2)
# getDoctorLink()
def getDetail():
    workbook=xlsxwriter.Workbook('安贞医院.xlsx')
    sheet=workbook.add_worksheet('安贞医院')
    row=['链接','姓名','照片','医院','科室','职称','擅长','职业经历']
    f2=open('detail_info.txt','w+',encoding='utf-8')
    for i in range(8):
        sheet.write(0,i,row[i])
    k=1
    for line in open('医生link.txt','r',encoding='utf-8'):
        line=eval(line)
        url='https:'+line[1]
        print(url)
        # break
        for t in range(5):
            try:
                bsObj=requests.get(url,headers=header,proxies=get_proxies_abuyun(),  timeout=15)
                bsObj=BeautifulSoup(bsObj.text,'html.parser')
                bsObj=bsObj.find_all('script')[3].get_text().replace('BigPipe.onPageletArrive(','').replace(')','').replace(';','')
                break
            except Exception as e:
                if '429' in str(e):
                    time.sleep(random.randint(0, 1000)/1000.0)
                continue
            # print(bsObj)
        bsObj=BeautifulSoup(json.loads(bsObj)['content'],'html.parser')
        about=bsObj.find('div',class_='middletr').find('table').find_all('tr',recursive=False)
        row=[url,line[0]]
        le=len(about)
        if le==6:
            print(about)
        print(le)
        if le==5:
            src='http:'+about[0].find('img').attrs['src']
            row.append(src)
            i=1
        else:
            row.append('')
            i=0
        for t in range(i,le):
            text=about[t].find_all('td')[2].get_text()
            if '医院' in text:
                text=text.split('医院')
                row=row+[text[0]+'医院',text[1]]
            else:
                try:
                    text=about[t].find_all('td')[2].find('div').get_text()
                except:
                    text=about[t].find_all('td')[2].get_text()
                row.append(text)
        print(row)
        f2.write(str(row)+'\n')
        for j in range(8):
            sheet.write(k,j,row[j])
        k=k+1
    workbook.close()

getDetail()        
