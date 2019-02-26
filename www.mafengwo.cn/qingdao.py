
from bs4 import BeautifulSoup
import requests
import csv
import sys
import util
from pandas import DataFrame,Series
import pandas as pd
sys.path.append("..")
import mytemp


urlRoot='http://www.mafengwo.cn/yj/10444/2-0-'
cookie='PHPSESSID=d8jjork1sdfla03t5vfn708qr6; mfw_uuid=5b728c09-93ad-8541-b9a7-d4f44bf3b2a8; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222018-08-14+16%3A00%3A09%22%3B%7D; uva=s%3A78%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1534233610%3Bs%3A10%3A%22last_refer%22%3Bs%3A6%3A%22direct%22%3Bs%3A5%3A%22rhost%22%3Bs%3A0%3A%22%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1534233610%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A0%3A%22%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5b728c09-93ad-8541-b9a7-d4f44bf3b2a8; UM_distinctid=1653773178143-08ac53b7b6bf12-b353461-100200-165377317823a2; CNZZDATA30065558=cnzz_eid%3D442987233-1534231255-%26ntime%3D1534236655; __mfwlv=1534241055; __mfwvn=2; __mfwlt=1534241138'

def main1():
    f=open('qd1.csv','w+',newline='',encoding='gb18030')
    csv_write=csv.writer(f)
    #708
    for i in range(0,708):
        newUrl=urlRoot+str(i)+'.html'
        print('正在爬取第'+str(i)+'页...')
        lilist=mytemp.getObj(newUrl,cookie).find('div',class_='post-list').find_all('li',class_='post-item clearfix')
        print(len(lilist))
        for li in lilist:
            a=li.find('h2').find_all('a')[-1]
            a1=li.find('span',class_='author').find_all('a')[-1]
            if 'href' not in  a.attrs:
                print('position error')
            else:
                wr=[a['href'],a.get_text(),a1['href'],a1.get_text()]
                # print(wr)
                csv_write.writerow(wr)


def main2():
    root2='http://www.mafengwo.cn'
    f_error1=open('logtime.txt','a+')
    f_error2=open('logplace.txt','a+')
    f1=open('qd1.csv','r',encoding='gb18030',newline='')
    f=open('qd2.csv','a+',newline='',encoding='gb18030')
    csv_write=csv.writer(f)
    for info in csv.reader(line.replace('\0','') for line in f1):
        newUrl=root2+info[0]
        html=util.build_proxy_request(newUrl)
        obj = BeautifulSoup(html.text,'html.parser')
        place=set()
        for p in obj.find_all('a',class_='_j_anchor'):
            place.add(p.get_text().strip())
        if place==set():
            print(newUrl+'没有景点')
            f_error2.write(newUrl)
            continue
        try:
            time=obj.find('li',class_='time').get_text().split('/')[1]
            day=obj.find('li',class_='day').get_text().split('/')[1]
        except:
            # recordtime=obj.find('span',class_='time')
            print(newUrl+'没有时间')
            f_error1.write(newUrl)
            continue
        
        row=[newUrl,info[1],time,day,' '.join(place)]
        print(row)
        csv_write.writerow(row)
        # break

    # '_j_anchor'
    # http://www.mafengwo.cn/i/10190062.html



def main3():
    # ```没有时间的处理
    # f_error3=open('logconfplace.txt','w+')
    # f_error4=open('notime.txt','w+')
    f1=open('logplace.txt','r',encoding='gb18030',newline='')
    f=open('qd2.csv','a+',newline='',encoding='gb18030')
    csv_write=csv.writer(f)
    text=f1.read()
    textlist=text.split('http')
    # print(textlist)
    print(len(textlist))
    for i in range(1,len(textlist)):       
        newUrl='http'+textlist[i]
        # newUrl='http://www.mafengwo.cn/i/1373402.html'
        # print(newUrl)
        html=util.build_proxy_request(newUrl)
        obj = BeautifulSoup(html.text,'html.parser')
        try:
            time=obj.find('li',class_='time').get_text().split('/')[1]
            day=obj.find('li',class_='day').get_text().split('/')[1]
        except:
            time=''
            day=''
        place=set()
        for p in obj.find_all('a',class_='_j_anchor'):
            place.add(p.get_text().strip())
        for p in obj.find_all('a',class_='_j_keyword_list'):
            place.add(p.get_text().strip())
        if place==set():   
            print(newUrl+'没有景点')
            # f_error3.write(newUrl)
            continue
        row=[newUrl,time,day,' '.join(place)]
        print(row)
        csv_write.writerow(row)
        # break
    
# 'http://www.mafengwo.cn/i/1373402.html'
def datawrite():
    f=open('final2.csv','r',newline='',encoding='gb18030')
    f1=open('final4.csv','w+',newline='',encoding='gb18030')
    f2=pd.read_csv('qdtime.csv')
    # print(f2.ix[0])
    csv_write=csv.writer(f1)
    t=0
    http://pagelet.mafengwo.cn/note/pagelet/headOperateApi?callback=jQuery181024024145522831364_1534321864996&params=%7B%22iid%22%3A%2210051902%22%7D&_=1534321865675
    http://pagelet.mafengwo.cn/note/pagelet/headOperateApi?callback=jQuery181003556652679826677_1534322676121&params=%7B%22iid%22%3A%2210188570%22%7D&_=1534322676779
    for info in csv.reader(line.replace('\0','') for line in f):
        if info[1]=='':
            t=t+1
            # link=info[0].replace('http://www.mafengwo.cn','')
            # try:
            #     info[1]=f2[f2['/i/9449757.html']==link].values[0][1]
            #     # print(info[1])
            # except:
                # print(info[0])
            # obj=mytemp.getObj(info[0],cookie)
            # html=util.build_proxy_request(info[0])
            # print(info[0])
            # obj = BeautifulSoup(html.text,'html.parser')
            # print(obj)
            time=''
            day=''
            
            # time=obj.find('span',class_='time').get_text().split(' ')[0]
            
            # try:
            #     # time=obj.find('li',class_='time').get_text().split('/')[1]
            #     # day=obj.find('li',class_='day').get_text().split('/')[1]
                
            #     time=obj.find('span',class_='time').get_text().split(' ')[0]
            # except:
            #     pass
            
            # info=[info[0],time,day,info[3]]
            # print(info)                
                # print(link)
                # pass
        
        csv_write.writerow(info)
        # print(info[1])
        # break
    print(t)


datawrite()

