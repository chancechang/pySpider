
from bs4 import BeautifulSoup
import requests
import csv
import sys
sys.path.append("..")
from urllib.error import HTTPError
import mytemp
import time

import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
import xlsxwriter

def phangetObj(url,sheet):
    # desire = DesiredCapabilities.PHANTOMJS.copy() 
    # for key, value in header.items(): 
    #     desire['phantomjs.page.customHeaders.{}'.format(key)] = value 
    # driver = webdriver.PhantomJS(desired_capabilities=desire, executable_path="phantomjs.exe",service_args=['--load-images=no'])#将yes改成no可以让浏览器不加载图片 
    driver =webdriver.PhantomJS()   
    #使用浏览器请求页面
    driver.get(url)
    # driver.add_cookie(header)
    #加载3秒，等待所有数据加载完毕
    time.sleep(3)
    #通过id来定位元素，
    #.text获取元素的文本数据
    # dl=driver.find_elements_by_css_selector("#searchLeftOptions")
    # dl=driver.find_element_by_id("bpr-guid-1537650")
    # print(dl)
    
    
    # education=bsObj.find('code',{'id':'bpr-guid-1537650'}).get_text()
    # data=json.loads(education)['data']
    # print(data)

    time.sleep(15)
    s1 = Select(driver.find_element_by_id('selectDataType'))  # 实例化Select
    s1.select_by_value('3')
    time.sleep(15)
    # print(s1.text)
    r=1
    # while True:
    pageSource=driver.page_source
    bsObj=BeautifulSoup(pageSource,"html.parser")
    divbox=bsObj.find('div',{'id':'tableId'})
    if divbox==None:
        print('sleep')
        time.sleep(3)
        phangetObj(url,sheet)
        return
        # break            
        # continue
    else:
        table=divbox.find('table')
        if table==None:
            print('sleep')
            time.sleep(3)
            phangetObj(url,sheet)           
            return

        if r==1:
            rname=table.find('tr').find_all('th')
            for c in range(len(rname)):
                sheet.write(0,c,rname[c].get_text())
        try:
            trlist=table.find_all('tr')[1:]
        except:
            print(r)

        # break
        for tr in trlist:
            tdlist=tr.find_all('td',recursive=False)
            for c in range(len(tdlist)):
                sheet.write(r,c,tdlist[c].get_text())
            r=r+1
        # break
        # dr= driver.find_element_by_id('tableId')          
        # next=dr.find_elements_by_tag_name("a")[-2]
        # print(next.text)
        # if '上' in next.text:
        #     print(r)
        #     driver.close()
        #     return
        # next.click()    
    driver.close()
    return None

filename='球队数据'
workbook=xlsxwriter.Workbook(filename+'.xlsx')

beginYear='15'
for t in range(4):
    year='20'+str(beginYear)+'-20'+str(int(beginYear)+1)
    sheet=workbook.add_worksheet(year)
    url='http://zq.win007.com/cn/TechList/'+str(year)+'/36.html'
    print(url)
    phangetObj(url,sheet)
    beginYear=str(int(beginYear)+1)
    # break
workbook.close()
    

def getjfen():
    for t in range(10):
        year='20'+str(beginYear)+'-20'+str(int(beginYear)+1)
        sheet=workbook.add_worksheet(year)

        url='http://zq.win007.com/cn/League/'+str(year)+'/36.html'
        # print(url)
        for i in range(5):
            bsObj=phangetObj(url)
            table=bsObj.find('table',{'id':'div_Table1'})
            if table!=None:
                break
        try:
            trlist=table.find_all('tr')[:21]
        except:
            print('error2')
            print(url)
            continue
        r=0
        for tr in trlist:
            tdlist=tr.find_all('td',recursive=False)
            for c in range(len(tdlist)):
                sheet.write(r,c,tdlist[c].get_text())
            r=r+1
        # break
        beginYear=str(int(beginYear)+1)
    workbook.close()        