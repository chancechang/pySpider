from bs4 import BeautifulSoup
import requests
import csv

def build_request(url):
    for i in range(5):
        try:
            req=requests.get(url,timeout=20)
            return req
        except:
            continue
    return None
    
url1='http://m.imdb.com/title/tt1590193/reviews?ref_=m_tt_urv'
dynamicurl1='http://m.imdb.com/title/tt1590193/reviews/_ajax?ref_=undefined&paginationKey='
url2='http://m.imdb.com/title/tt6802308/reviews?ref_=m_tt_urv'
dynamicurl2='http://m.imdb.com/title/tt6802308/reviews/_ajax?ref_=undefined&paginationKey='
   
def dynamiCrawl(url,dynamicurl,csv_write):  
    req=build_request(url)
    req.encoding='utf-8'
    soup=BeautifulSoup(req.text,'html.parser')
    reviews=soup.find('div', {'id': 'reviews-container'}).find_all('li',class_='ipl-content-list__item')
    for review in reviews:
        userName=review.find('span',class_='display-name-link').string
        time=review.find('span',class_='review-date').string
        if review.find('span',class_='rating-other-user-rating'):
            score=review.find('span',class_='rating-other-user-rating').find('span').string+'.0 / 10'
        else:
            score=''
        title=review.find('span',class_='title').string
        
        if review.find('span',class_='spoiler-warning__control ipl-expander__control'):
            text=review.find('span',class_='spoiler-warning__control ipl-expander__control').string
        else:
            text=review.find('div',class_='text').get_text()
        print(score,title,userName,time)
        csv_write.writerow([score,title,userName,time,text])
    if soup.find('div',class_='load-more-data'): 
        dataKey=soup.find('div',class_='load-more-data')['data-key']
        print(dataKey)
        dynamiCrawl(dynamicurl+dataKey,dynamicurl,csv_write)

#csv文件的写入

def writetoCsv(filename,url,dynamicurl):
    out=open(filename, 'w+',encoding='gb18030',newline = '')
    csv_write=csv.writer(out)
    csv_write.writerow(['评分','评论题目','用户名','时间','评论内容'])
    dynamiCrawl(url,dynamicurl,csv_write)      
        
writetoCsv('imdbcommuter.csv',url1,dynamicurl1)
writetoCsv('imdbparis.csv',url2,dynamicurl2)

import csv
#csv文件的读取
def csvRead(filename):   
    csv_reader = csv.reader(open(filename, encoding='gb18030'))
    for row in csv_reader:
        username=row[0]
        url=row[1]
        print(row[1])
        # crawl(username,url)



import urllib.request
import json

cook='_zap=103062c2-b140-4bb3-9b09-c6cf339bb388; d_c0="AECCyMfSwQyPTpKO0aCmkPUGPKluXFgq_Bw=|1511945695"; __DAYU_PP=EbUEJqyeeFNufYfVivYR2ba2111a3034; _xsrf=342e908a-93bd-4e26-bb31-ee4cb0e42acb; q_c1=deb5f34c9c784ae5b70a9cae0b24ee5d|1521542185000|1501208857000; capsion_ticket="2|1:0|10:1521558824|14:capsion_ticket|44:MjEwZjI4NTI4Mjk2NGRkZWFiMWZjY2JjY2I3Mjk0NjA=|629b05c7a8cb266f450ffe58788e2c07e56051bdcc00b7957f702bd49017e4c5"; z_c0="2|1:0|10:1521558888|4:z_c0|92:Mi4xdDlrX0FnQUFBQUFBUUlMSXg5TEJEQ1lBQUFCZ0FsVk5hSE9lV3dCaHRfdnRXbnYzc3FiRGdFZUpBMW1CcmstUFZ3|f3cebdebc483f14d2bab9d9f4048d79bd5f77237fe51453a66c2a90d8bf8d54d"; unlock_ticket="ABCK5wre8ggmAAAAYAJVTXAssVpzFDh0uhrcnxHvYPpchsYSmNRR_g=="'
headers = {
    "Cookie":cook,
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}


#获取json文件方法
def getJson(url):
    #获取json
    f= urllib.request.Request(url,headers=headers)
    html=urllib.request.urlopen(f).read().decode('utf-8',"ignore")
    #post方法请求json数据
    r = requests.post(url, data = {'cityCode':citycode,'page':page})
    try:
        data=json.loads(r.text)["BusinessHallList"]  
    return data

import urllib.request
from urllib.error import HTTPError
import requests
def getObj(url):
    try:
        html=requests.get(url,headers=headers)
        html.encoding="utf-8"
    except HTTPError as e:
        print('HTTPError')
        return None
    try:
        bsObj = BeautifulSoup(html.text,'html.parser')
    except AttributeError as e:
        print('AttributeError')
        return None
    return bsObj


from selenium import webdriver
#可用来解决js渲染的重定向数据抓取不到问题
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
    bsObj=BeautifulSoup(pageSource,"html.parser")
    crawl(bsObj,f,city,indu,r)   
    driver.close()

import xlwt
#写入excel
data=xlwt.Workbook()
table=data.add_sheet(indu.replace("/","_"),cell_overwrite_ok=True)
r=0
row=[]
for i in range(0,len(row)):
    table.write(r,i,row[i])
data.save("test.xls")


#解析本地html文件
from bs4 import BeautifulSoup
bsObj = BeautifulSoup(open('2016.html','r',encoding='utf-8').read(),'html.parser')


