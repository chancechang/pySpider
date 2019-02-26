from bs4 import BeautifulSoup
import requests
import csv
import sys
sys.path.append("..")
import mytemp
import util
import re
from pandas import Series,DataFrame
import pandas as pd
import time

def get_city_mag():
    #城市信息链接
    urlroot1='https://www.baidu.com/sf?openapi=1&dspName=iphone&from_sf=1&pd=city&ms=1&hide=1&apitn=tangram&top=%7B%22sfhs%22%3A2%7D&tfr=redis&resource_id=4324&word='
    urlroot2='&title=%E7%9B%AE%E7%9A%84%E5%9C%B0%E6%94%BB%E7%95%A5&city_name=&frsrcid=&frorder=&lid=&ext=%7B%22sf_tab_name%22%3A%22%E6%A6%82%E8%A7%88%22%7D&sa=sf_tab1'

    fRead=open('city.csv','r',encoding='gb18030')
    f_city_msg=open('city_msg.csv','w+',newline='',encoding='gb18030')
    f_error=open('city_error.txt','w+')
    csv_write=csv.writer(f_city_msg)
    csv_write.writerow(['城市','链接','缩略图链接','适宜季节','百度百科','',''])
    for line in csv.reader(fRead):
        try:
            newUrl=urlroot1+line[0]+urlroot2
            req=util.build_proxy_request(newUrl)
            bsObj=BeautifulSoup(req.text,'html.parser')
            div=bsObj.find('div',class_='ly-city')
            image_link=div.find('div',class_='c-row-tile c-gap-bottom ly-city-info-position').find('img').attrs['src']
            suit_season=div.find('div',class_='c-line-clamp1 c-span6').get_text().replace('适宜季节：','')
            bdbk=div.find('span',class_='c-color').get_text()
            row=[line[0],newUrl,image_link,suit_season,bdbk]
            print(row)
            csv_write.writerow(row)
        except:
            print(newUrl)
            f_error.write(newUrl+'\n')

def get_city_again():
    f_city_msg=open('city_msg.csv','a+',newline='',encoding='gb18030')
    csv_write=csv.writer(f_city_msg)
    f_error=open('city_error2.txt','w+')
    for line in open('city_error1.txt','r'):
        # print(line)
        try:
            newUrl=line
            city=re.search(r'word=(.+?)&',newUrl).group(1)
            req=util.build_proxy_request(newUrl)
            bsObj=BeautifulSoup(req.text,'html.parser')
            div=bsObj.find('div',class_='ly-city')
            image_link=div.find('div',class_='c-row-tile c-gap-bottom ly-city-info-position').find('img').attrs['src']
            try:
                suit_season=div.find('div',class_='c-line-clamp1 c-span6').get_text().replace('适宜季节：','').replace('建议游玩：','')
            except:
                suit_season=''
            try:
                bdbk=div.find('span',class_='c-color').get_text()
            except:
                bdbk=div.find('div',class_='c-color c-line-clamp3').get_text()
            row=[city,newUrl,image_link,suit_season,bdbk]
            print(row)
            csv_write.writerow(row)
        except:
            print(newUrl)
            f_error.write(newUrl+'\n')
         


def getAttractions():
    urlroot3='https://www.baidu.com/sf?openapi=1&dspName=iphone&from_sf=1&pd=city&ms=1&hide=1&apitn=tangram&top=%7B%22sfhs%22%3A2%7D&tfr=redis&resource_id=4336&word='
    urlroot4='&title=%E7%9B%AE%E7%9A%84%E5%9C%B0%E6%94%BB%E7%95%A5&city_name=&frsrcid=&frorder=&lid=&ext=%7B%22sf_tab_name%22%3A%22%E6%99%AF%E7%82%B9%22%7D&sa=sf_tab1'
    fRead=open('city.csv','r',encoding='gb18030')
    f_attractions_msg=open('attractions_msg_first.csv','w+',newline='',encoding='gb18030')
    f_error=open('attractions_get_error.txt','w+')
    csv_write=csv.writer(f_attractions_msg)
    csv_write.writerow(['城市','城市链接','景点','景点链接','缩略图链接','评分','简介','',''])
    for line in csv.reader(fRead):
        rowlist=[]
        try:
            newUrl=urlroot3+line[0]+urlroot4
            req=util.build_proxy_request(newUrl)
            bsObj=BeautifulSoup(req.text,'html.parser')
            divlist=bsObj.find('div',class_='sfc-ly-scene-list-wrap').find_all('div',class_='sfc-ly-scene-list-item c-container WA_LOG_SF')
            for div in divlist:
                name=div.find('span',class_='sfc-ly-scene-list-item-name').get_text()
                link=div.attrs['data-href']
                img_link=div.find('div',class_='c-img c-img-z').find('img').attrs['src']
                score=div.find('span',class_='sfc-ly-scene-list-item-score').get_text()
                introduction=div.find('p',class_='c-line-clamp2 sfc-ly-scene-list-item-desc').get_text()
                row=[line[0],newUrl,name,link,img_link,score,introduction]
                rowlist.append(row)                
            for r in rowlist:
                csv_write.writerow(r)
            print(line[0]+'已写入')
        except:
            print(newUrl)
            f_error.write(newUrl+'\n')
# getAttractions()

def get_detail():
    fRead=open('attractions_msg_first.csv','r',encoding='gb18030')
    f_attractions_msg=open('attractions_msg_final.csv','a+',newline='',encoding='gb18030')
    csv_write=csv.writer(f_attractions_msg)
    headrow=['城市','城市链接','景点','景点链接','缩略图链接','评分','简介','百度百科','开放时间','门票信息','游玩时长','最佳季节','官网','电话','地址']
    # csv_write.writerow(headrow)
    # f_error1=open('attractions_get_error_link1.csv','w+')
    # csv_write1=csv.writer(f_error1)
    # f_error2=open('attractions_get_error_link2.csv','w+')
    # csv_write1=csv.writer(f_error2)

    for line in csv.reader(fRead):
        error=0
        line=line[:7]
        # print(line)
        row=line+['' for i in range(14) ]
        # try:
        newUrl=line[3]
        # newUrl='http://m.baidu.com/sf?openapi=1&dspName=iphone&from_sf=1&pd=jingdian_detail&resource_id=4616&word=%E9%9D%92%E6%B5%B7%E8%97%8F%E6%96%87%E5%8C%96%E9%A6%86&title=%E9%9D%92%E6%B5%B7%E8%97%8F%E6%96%87%E5%8C%96%E9%A6%86&lid=9159143487664320820&ms=1&frsrcid=31132&frorder=6'
        print(line[0],line[2])
        for i in range(3):
            bsObj=mytemp.getObj(newUrl)
            # req=util.build_proxy_request(newUrl)
            # bsObj=BeautifulSoup(req.text,'html.parser')
            div=bsObj.find('div',class_='c-list')   
            if div!=None:
                break
        if div==None:
            csv_write.writerow(line)
            continue
        try:                                          
            bdbk=div.find('div',class_='c-list-item c-line-bottom c-list-border').get_text().replace('百度百科','')
        except:
            try:
                bdbk=div.find('div',class_='c-color c-gap-bottom c-line-clamp3').get_text().replace('百度百科','') 
            except:
                bdbk=''                  
        row[7]=bdbk

        divlist1=div.find_all('div',class_='c-gap-inner-top c-flexbox c-line-bottom c-gap-inner-bottom')
        divlist2=div.find_all('div',class_='c-gap-inner-top c-flexbox')
        for d in divlist1:
            dlist=d.find_all('div') 
            title=dlist[0].get_text().strip()
            text=d.find('div',class_='c-span12').get_text().strip()
            try:
                t=headrow.index(title)
                row[t]=text
            except:
                headrow.append(title)
                t=headrow.index(title)
                row[t]=text
        for d in divlist2:  
            dlist=d.find_all('div') 
            title=dlist[0].get_text().strip()
            try:
                text=d.find('div',class_='c-span12').find('a').attrs['href'].replace('Tel:','')
            except:
                text=d.find('div',class_='c-span12').get_text().strip()
            try:
                t=headrow.index(title)
                # print(t)
                row[t]=text
            except:
                headrow.append(title)
                print(headrow)
                t=headrow.index(title)                
                row[t]=text   
        csv_write.writerow(row)
        # break
    print(headrow)


def get_error_link1():
    # # names=['城市','城市链接','景点','景点链接','缩略图链接','评分','简介'],
    # data1=pd.read_csv('attractions_msg_first.csv',header=None,encoding='gb18030')  
    # data2=pd.read_table('attractions_get_error_link1.txt',header=None,encoding='gb18030')
    # data=pd.merge(data1,data2,left_on=3,right_on=0)
    # # find('div',class_='c-color c-gap-bottom c-line-clamp3')
    # data.to_csv('error.csv', sep='*',encoding='gb18030')
    f_attractions_msg=open('attractions_msg_final.csv','a+',newline='',encoding='gb18030')
    csv_write=csv.writer(f_attractions_msg)
    headrow=['城市','城市链接','景点','景点链接','缩略图链接','评分','简介','百度百科','开放时间','门票信息','游玩时长','最佳季节','官网','电话','地址']
    f_error3=open('error3.csv','w+',encoding='gb18030',newline='')
    f_error2=open('error4.txt','w+')
    csv.write1=csv.writer(f_error3)

    data1=pd.read_csv('attractions_msg_first.csv',header=None,encoding='gb18030')
    for attractions_link in open('attractions_get_error_link1.txt','r'):
        error=0
        r=data1[data1[3]==attractions_link.strip()].values[0][:6]
        row=list(r)+['' for i in range(20) ]
        newUrl=attractions_link
        # newUrl='http://m.baidu.com/sf?openapi=1&dspName=iphone&from_sf=1&pd=jingdian_detail&resource_id=4616&word=%E9%9D%92%E6%B5%B7%E8%97%8F%E6%96%87%E5%8C%96%E9%A6%86&title=%E9%9D%92%E6%B5%B7%E8%97%8F%E6%96%87%E5%8C%96%E9%A6%86&lid=9159143487664320820&ms=1&frsrcid=31132&frorder=6'
        print(newUrl)
        for i in range(3):
            try:
                bsObj=mytemp.getObj(newUrl)
                # req=util.build_proxy_request(newUrl)
                # bsObj=BeautifulSoup(req.text,'html.parser')
                div=bsObj.find('div',class_='c-list') 
                try:                                          
                    bdbk=div.find('div',class_='c-list-item c-line-bottom c-list-border').get_text().replace('百度百科','')
                except:
                    try:
                        bdbk=div.find('div',class_='c-color c-gap-bottom c-line-clamp3').get_text().replace('百度百科','') 
                    except:
                        bdbk=''                  
                break
            except:
                time.sleep(2)
                # pass
                
            if i==4:
                print('error1')
                error=1
                csv.write1.writerow(r) 
        if error==1:
            continue 
        try:
            divlist1=div.find_all('div',class_='c-gap-inner-top c-flexbox c-line-bottom c-gap-inner-bottom')
            divlist2=div.find_all('div',class_='c-gap-inner-top c-flexbox')
            # print(divlist2)
            for d in divlist1:
                dlist=d.find_all('div') 
                title=dlist[0].get_text().strip()
                text=d.find('div',class_='c-span12').get_text().strip()
                try:
                    t=headrow.index(title)
                    row[t]=text
                except:
                    headrow.append(title)
                    t=headrow.index(title)
                    row[t]=text
            for d in divlist2:  
                dlist=d.find_all('div') 
                title=dlist[0].get_text().strip()
                try:
                    text=d.find('div',class_='c-span12').find('a').attrs['href'].replace('Tel:','')
                except:
                    text=d.find('div',class_='c-span12').get_text().strip()
                try:
                    t=headrow.index(title)
                    # print(t)
                    row[t]=text
                except:
                    headrow.append(title)
                    print(headrow)
                    t=headrow.index(title)                
                    row[t]=text   
        except:
            print('error2')
            f_error2.write(r+'\n')
        # print(row)
        csv_write.writerow(row)
        # break
    print(headrow)



def get_gps():
    fRead=open('attractions_msg_final.csv','r',encoding='gb18030')
    f_attractions_msg=open('attractions_msg_final1.csv','a+',newline='',encoding='gb18030')
    csv_write=csv.writer(f_attractions_msg)
    headrow=['城市','城市链接','景点','景点链接','缩略图链接','评分','简介','百度百科','开放时间','门票信息','游玩时长','最佳季节','官网','电话','地址','交通','gps_链接']
    # csv_write.writerow(headrow)
    for line in csv.reader(fRead):
        for i in range(8,12):
            t=line[i]
            if t!='':
                line[i]=t[:int(len(t)/2)]   

        if line[14]!='':
            continue
        line=line[:16]+['']  
        newUrl=line[3]
        print(newUrl)
        for i in range(3):
            bsObj=mytemp.getObj(newUrl)
            # req=util.build_proxy_request(newUrl)
            # bsObj=BeautifulSoup(req.text,'html.parser')
            div=bsObj.find('div',class_='c-list')   
            if div!=None:
                break
        if div==None:
            csv_write.writerow(line)
            continue
        divlist2=div.find_all('div',class_='c-gap-inner-top c-flexbox')
        for d in divlist2:  
            dlist=d.find_all('div') 
            title=dlist[0].get_text().strip()
            if title!='电话':
                continue                
            try:
                text=d.find('div',class_='c-span12').find('a').attrs['href'].replace('Tel:','')
            except:
                text=d.find('div',class_='c-span12').get_text().strip()
            line[13]='_'+text
        try:
            gps_link=bsObj.find('div',class_='c-img c-img-item c-img-v').find('img').attrs['src']
            
        except:
            gps_link=''
            print('gps_link_error')
        try:
            address=bsObj.find('div',class_='map-address c-gap-top').find('p',class_='map-address-text').get_text()
            
        except:
            address=''
            print('address_error')
        try:
            traffic=bsObj.find('div',class_='map-traffic c-gap-top').find('div',class_='map-traffic-container').get_text().replace('交通','').strip()
            
        except:
            traffic=''
            print('traffic_error')
        if line[15]=='':
            line[15]=traffic
        line[14]=address
        line[16]=gps_link
        csv_write.writerow(line)
      
# get_gps()  

def get_lat_lon():
    fRead=open('attractions_msg_final1.csv','r',encoding='gb18030')
    f_attractions_msg=open('attractions_msg_final_final.csv','w+',newline='',encoding='gb18030')
    csv_write=csv.writer(f_attractions_msg)
    headrow=['城市','城市链接','景点','景点链接','缩略图链接','评分','简介','百度百科','开放时间','门票信息','游玩时长','最佳季节','官网','电话','地址','交通','gps_链接']
    csv_write.writerow(headrow)
    for line in csv.reader(fRead):
        if line[16]=='':
            csv_write.writerow(line)
            continue
        # print(line[16])
        lat_lon=re.search(r'center=(.+?)&',line[16]).group(1)
        csv_write.writerow(line+lat_lon.split(','))
        # print(lat_lon.split(','))
        # break
# get_lat_lon()
# Latitude and longitude

def merge_csv():
    #所有信息 地址的
    fRead=open('attractions_msg_final.csv','r',encoding='gb18030')
    # data1=pd.read_csv('attractions_msg_final_final.csv',encoding='gb18030')

    f_attractions_msg=open('attractions_msg_final2.csv','w+',newline='',encoding='gb18030')
    csv_write=csv.writer(f_attractions_msg)

    for line in csv.reader(fRead):  
        for i in range(8,12):
            t=line[i]
            if t!='':
                line[i]=t[:int(len(t)/2)]   
        if line[13]!='':     
            line[13]='_'+line[13]    
        if line[14]!='':
            # print(line)
            csv_write.writerow(line)
        # else:
        #     r=data1[data1[3]==line[3].strip()].values[0]
        #     print(r)
        #     csv_write.writerow(r)
            
merge_csv()