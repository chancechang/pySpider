
import requests
import csv
import json
import mytemp
import re
import time

def main5():
    '获取个人信息页'
    f5=open('personal_info.csv','w+',newline='',encoding='gb18030')
    csv_write5=csv.writer(f5)
    # f6=open('personal_info.txt','w+',encoding='utf-8')
    for i in range(1,13):
        print(i)
        url='http://zupu.syshenshi.com/ZR.aspx?pageindex='+str(i)+'&infoname=&mobile=&infotype=&infotype_name=&industry=&address=&iswaiqian=0&fuqin=&muqin=&peiou=&zinv=&muyuandizhi=&waiqiandizhi=&chushengriqi_begin=&chushengriqi_end=&qushiriqi_begin=&qushiriqi_end=&waiqian_begin=&waiqian_end='
        try:
            bsObj=mytemp.getObj(url)
            trlist=bsObj.find('table',class_='stdtable').find('tbody').find_all('tr')
        except:
            time.sleep(10)
            try:
                bsObj=mytemp.getObj(url)
                trlist=bsObj.find('table',class_='stdtable').find('tbody').find_all('tr')
            except:
                time.sleep(10)
                bsObj=mytemp.getObj(url)
                trlist=bsObj.find('table',class_='stdtable').find('tbody').find_all('tr')
        for tr in trlist:
            tdlist=tr.find_all('td')
            row=[]
            for td in tdlist:
                if td.find('a')!=None:
                    row.append(td.find('a').attrs['href'])
                row.append(td.get_text())
            # f6.write(str(row)+'\n')
            csv_write5.writerow(row)
            
main5()       
