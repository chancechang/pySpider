# coding=utf-8
# http://www.fortunechina.com/fortune500/c/2017-07/20/content_286785.htm
# http://www.fortunechina.com/fortune500/c/2016-07/20/content_266955.htm
# http://www.fortunechina.com/fortune500/c/2015-07/22/content_244435.htm
# http://www.fortunechina.com/fortune500/c/2014-07/07/content_212535.htm
# http://www.fortunechina.com/fortune500/c/2013-07/08/content_164375.htm
# http://www.fortunechina.com/fortune500/c/2013-07/08/content_164375_2.htm
# http://www.fortunechina.com/fortune500/c/2013-07/08/content_164375_5.htm
import requests
from bs4 import BeautifulSoup
import csv
from urllib.error import HTTPError
from selenium import webdriver
import time
def phangetObj(url):
    driver =webdriver.PhantomJS(executable_path="phantomjs.exe")   
    #使用浏览器请求页面
    driver.get(url)
    #加载3秒，等待所有数据加载完毕
    time.sleep(3)
    #通过id来定位元素，
    #.text获取元素的文本数据
    # dl=driver.find_elements_by_css_selector("#searchLeftOptions")
    pageSource=driver.page_source
    bsObj = BeautifulSoup(pageSource,'html.parser')
    getlink(bsObj,url)
    driver.close()

cook='_ga=GA1.2.932664684.1527155572; _gid=GA1.2.564882170.1527402650'
headers = {
    "Cookie":cook,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept - Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    # 'Connection':'keep-alive',
    # 'Upgrade-Insecure-Requests':1,
    # 'Host':'www.fortunechina.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',}

def getObj(url):
    '''获取网页并解析
    '''
    try:
        html=requests.get(url,headers=headers)
        html.encoding='utf-8'
        print(html.status_code)
    except HTTPError as e:
        print('HTTPError')
        return None
    try:
        bsObj = BeautifulSoup(html.text,'html.parser')
        # bsObj = BeautifulSoup(open('2014.html','r',encoding='utf-8').read(),'html.parser')
    except AttributeError as e:
        print('AttributeError')
        return None
    return bsObj

def getlink(trlist,url):
    trlist=trlist.find('table',{'id':'yytable'}).find_all('tr')
    filename='fortune1'+url[url.find('201'):url.find('201')+4]+'.txt'
    f=open(filename,'w+',encoding='utf-8')

    for tr in trlist:
        tdlist=tr.find_all('td')
        if len(tdlist)!=6:
            continue
            print(tdlist)
            print("warning")
        if 'href' in tdlist[2].find('a').attrs:
            href=tdlist[2].find('a').attrs['href']
        else:
            href=''
        warray=[href]
        for td in tdlist:
            warray.append(td.get_text().strip())
        f.write(str(warray)+'\n')
#2017-2014可用 
url17='http://www.fortunechina.com/fortune500/c/2017-07/20/content_286785.htm'
url16='http://www.fortunechina.com/fortune500/c/2016-07/20/content_266955.htm'
url15='http://www.fortunechina.com/fortune500/c/2015-07/22/content_244435.htm'
# url14='http://www.fortunechina.com/fortune500/c/2014-07/07/content_212535.htm'
url14='http://www.fortunechina.com/fortune500/c/2014-07/07/content_212535.htm'
phangetObj(url16)
url13='http://www.fortunechina.com/fortune500/c/2013-07/08/content_164375_2.htm'
#2013
def getlink13()

def getdetail(filename):
    out=open(filename[:-4]+'.csv', 'w+',encoding='gb18030',newline = '')
    csv_write=csv.writer(out)
    csv_write.writerow(['英文名','中文名','国家','营业收入','利润','资产','股东权益','净利率','资产收益率','人数','总部所在城市','CEO'])

    for line in open(filename,'r',encoding='utf-8'):
        csvWlist=[]
        domain='http://www.fortunechina.com'
        line=eval(line)
        url=domain+line[0][11:]
        name=line[3].split('（')
        csvWlist.append(name[0])
        csvWlist.append(name[1][:-1])
        csvWlist.append(line[6])
        csvWlist+=line[4:6]
        obj=getObj(url).find('div',class_='articlemain')
        print(obj)


        print(csvWlist)
        break
# getdetail('fortune2017.txt')
