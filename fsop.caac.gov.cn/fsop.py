

import requests
import csv
import json
import sys
sys.path.append("..")
import mytemp
import re
import time


def main():
    M={}
    M['民航局CAAC']='402881fa2c3e722b012c3e7b56a00005'
    M['华北地区管理局']='402881fa2c954d54012c954d54530000'
    M['东北地区管理局']='402881fb2c965e73012c965e73e20000'
    M['华东地区管理局']='402881fb2c965e73012c965ee4200001'
    M['中南地区管理局']='402881fb2c965e73012c965f5ac70002'
    M['西南地区管理局']='402881fb2c965e73012c965fc8940003'
    M['西北地区管理局']='402881fb2c965e73012c966030570004'
    M['新疆管理局']='402881fb2c965e73012c9660d9b60005'
    f1=open('fsop_link.txt','a+',encoding='utf-8')

    for key,value in M.items():
        for i in range(30):
            print(key,i)
            url='http://fsop.caac.gov.cn/g145/CARS/WebSiteQueryServlet?method=enterpriseQuery&iDisplayStart='+str(i*20)+'&iDisplayLength=20&orgId='+value
            req=requests.get(url)
            data=json.loads(req.text)['aaData']
            le=len(data)
            print(le)        
            if le==0:
                break
            for i in range(le):
                d=data[i]
                enterpriseName=d['enterpriseName']
                licenceCode=d['licenceCode']
                enterpriseId=d['enterpriseId']
                row=[key,enterpriseName,licenceCode,enterpriseId]
                # print(row)
                f1.write(str(row)+'\n')
def main1():
    f2=open('up_info.csv','a+',encoding='gb18030',newline='')
    csv_write2=csv.writer(f2)
    
    for line in open('fsop_link.txt','r',encoding='utf-8'):
        line=eval(line)
        print(line[3])
        url='http://fsop.caac.gov.cn/g145/CARS/WebSiteQueryServlet?method=loadEnterpriseDetail&enterpriseId='+line[3]
        bsObj=mytemp.getObj(url)
        # print(bsObj)
        t=re.search(r'\$.trim((.+?))}',str(bsObj)).group(1)
        # print(t)
        # break
        divlist=bsObj.find('div','am-u-md-10').find_all('div',class_='am-g am-margin-top')
        address=divlist[2].find('div',class_='am-u-sm-8 am-u-md-8 am-u-end').get_text().replace('\t','').replace('\n','').replace('\xa0','').replace('\r','').strip()
        expirated=divlist[3].find('div',class_='am-u-sm-8 am-u-md-8 am-u-end').get_text().replace('\t','').replace('\n','').replace('\r','').strip().split(' ')[0]
        scan=divlist[4].find('div',class_='am-u-sm-8 am-u-md-8 am-u-end')
        Scannedname=scan.get_text().replace('\t','').replace('\n','').replace('\r','').strip()
        try:
            Scannedurl='http://fsop.caac.gov.cn'+scan.find('a').attrs['href']
        except:
            Scannedurl=''
        Limited=divlist[5].find('div',class_='am-u-sm-8 am-u-md-8 am-u-end').get_text().replace('\t','').replace('\n','').replace('\r','').strip()
        row=[url,t]+line[:3]+[address,expirated,Scannedname,Scannedurl,Limited]
        # print(row)
        csv_write2.writerow(row)
        # break
        # break
def main3():
    f3=open('fsop_add.csv','w+',encoding='gb18030',newline='')
    csv_write3=csv.writer(f3)
    # for line in csv.reader(open('up_info.csv','r',encoding='utf-8')):
    #     id=line[1].replace(')','').replace('(','').replace('"','')
    #     print(str(line[2:4]))
    i=58
    id='796dad71-1608c2280cd-a8c051a458585a91f6bbafef906370ff'
        # time.sleep(5)
        # while True:
    url='http://fsop.caac.gov.cn/g145/CARS/WebSiteQueryServlet?method=aircraftQuery&iColumns=9&sColumns=&iDisplayStart='+str(i*20)+'&iDisplayLength=20&mDataProp_0=categoryNo&mDataProp_1=partsNumber&mDataProp_2=partsName&mDataProp_5=5&licenceId='+id
    try:
        req=requests.get(url)
    except:
        time.sleep(10)
        try:
            req=requests.get(url)
        except:
            time.sleep(10)
            req=requests.get(url)

    data=json.loads(req.text)['aaData']
    le=len(data)
    print(i,le)
    for d in data:
        categoryNo=d['categoryNo']
        partsNumber=d['partsNumber']
        partsName=d['partsName']
        ataChaptersection=d['ataChaptersection']
        manufacturers=d['manufacturers']
        statu=''
        if d['inspection']=='1':
            statu=statu+'inspection  '
        inspection=d['inspection']
        if d['modification']=='1':
            statu=statu+'modification  '
        if d['repair']=='1':
            statu=statu+'repair'
        fileToAccord=d['fileToAccord']
        mainDevices=d['mainDevices']
        remark=d['remark']
        row=[categoryNo,partsNumber,partsName,ataChaptersection,manufacturers,statu,fileToAccord,mainDevices,remark]
        # print(row)
        csv_write3.writerow(row)
            # i=i+1
            # if le<20:
            #     break
            #     break
# main3()