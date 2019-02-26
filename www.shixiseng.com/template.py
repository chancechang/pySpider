from bs4 import BeautifulSoup
import requests
import csv

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


from urllib.error import HTTPError
import requests

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


