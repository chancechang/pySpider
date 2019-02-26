from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time

#可用来解决js渲染的重定向数据抓取不到问题
def phangetObj(url,crawl,data=None):
    driver =webdriver.PhantomJS(executable_path="phantomjs.exe")   
    #使用浏览器请求页面
    driver.get(url)
    #加载3秒，等待所有数据加载完毕
    time.sleep(3)
    targetMsg=crawl(driver) 
    driver.close()
    return targetMsg

def crawl(driver):
    targetdata=[]
    pageSource=driver.page_source
    bsObj=BeautifulSoup(pageSource,"html.parser")
    # print(bsObj)
    obj=bsObj.find('ul',class_='carlist clearfix js-top').findAll('li')
    for li in obj:
        a=li.find('a')
        listname=a['title']
        href='https://www.guazi.com'+a['href']
        div1_text=a.find('div',class_='t-i').get_text().split('|')
        price=a.find('div',class_='t-price').get_text()
        targetdata.append([listname,href]+div1_text+[price])
    return targetdata
def writetoCsv(filename,writelist,header=None):
    out=open(filename, 'w+',encoding='gb18030',newline = '')
    csv_write=csv.writer(out)
    if header!=None:
        csv_write.writerow(header)
    for wlist in writelist:
        csv_write.writerow(wlist)

url='https://www.guazi.com/gz/bmw-x5/p0-80/'
targetdata=phangetObj(url,crawl)
writetoCsv('gzbmX5.csv',targetdata,['标题','链接','年份','里程','价格'])