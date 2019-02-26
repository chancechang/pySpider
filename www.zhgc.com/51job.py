from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
import time
from urllib.error import HTTPError
import urllib.request

cityCode='020000'
#若要使用代理，改为TRUE，补充get_proxies_abuyun函数中代理渠道验证信息
proxy=False
beginPage=1

urlroot='https://search.51job.com/list/'



def getObj(url,proxyIs=False,cook=None,encode='gbk'):
    for i in range(5):
        try:
            if cook==None:
                if proxyIs==False:
                    html=requests.get(url)
                else:
                    html=util.build_proxy_request(url)
            else:
                if proxyIs==False:
                    html=requests.get(url,headers=getHeaders(cook),verify=False)
                else:
                    header=getHeaders(cook)
                    html=util.build_proxy_request(url,None,getHeaders,None)
            html.encoding=encode  
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

def get_proxies_abuyun():
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"
    # 代理隧道验证信息
    proxyUser = ''
    proxyPass = ''

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

f1=open('51job.csv','w+',encoding='gb18030',newline='')
csv_write=csv.writer(f1)
csv_write.writerow(['职位名','职位链接','公司名','公司链接','工作地点','薪资','发布时间'])
for i in range(beginPage,2001):
    url=urlroot+cityCode+',000000,0000,00,1,99,%2B,2,'+str(i)+'.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=5&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    

    if proxy==True:
        proxies=get_proxies_abuyun()
        for m in range(5):
            try:
                html=requests.get(url,proxies=proxies, timeout=15)
                break
            except Exception as e:
                if '429' in str(e):
                    time.sleep(random.randint(0, 1000)/1000.0)
                continue
            bsObj=BeautifulSoup(html.text,'html.parser')
    else:
        bsObj=getObj(url)
    try:
        divlist=bsObj.find('div',{'id':'resultList'}).find_all('div',class_='el')
    except:
        print('第'+str(i)+'页失效')
        continue
    for div in divlist:
        positionName=''   
        positionlink=''
        try:
            p=div.find('p',class_='t1')
            positionName=p.get_text().replace('\n','').strip()      
            positionlink=p.find('a').attrs['href']
        except:
            continue
        span=div.find('span',class_='t2')
        companyName=''
        companyLink=''
        if span!=None:
            companyName=span.get_text()
            companyLink=span.find('a').attrs['href']
        try:
            local=div.find('span',class_='t3').get_text()
        except:
            local=''
        try:
            salary=div.find('span',class_='t4').get_text()
        except:
            salary=''
        try:
            publishTime=div.find('span',class_='t5').get_text()
        except:
            publishTime=''
        row=[positionName,positionlink, companyName,companyLink ,local,salary,publishTime]
        print(row)
        csv_write.writerow(row)

