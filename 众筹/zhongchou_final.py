

from bs4 import BeautifulSoup
import requests
import csv
import time
import json
import re


url='http://www.zhongchou.cn/browse/re-sb-p'
filename='众筹项目'
max_page=292

def getObj(url,encode='utf-8'):
    for i in range(5):
        try:
            html=requests.get(url)
            html.encoding=encode  
            break
        except:
            time.sleep(10)
            print('再次请求')
            print('HTTPError')
            return None
    try:
        bsObj = BeautifulSoup(html.text,'html.parser')
    except:
        print('AttributeError')
        return None
    return bsObj

def getLink():
    f1=open(filename+'.csv','w+',newline='',encoding='gb18030')
    csv_write=csv.writer(f1)
    for i in range(4,max_page):
        print('正在爬取第'+str(i)+'页')
        newurl=url+str(i)
        bsObj=getObj(newurl).find('div',class_='sousuoListBox clearfix')
        divlist=bsObj.find_all('div',class_='ssCardItem')
        print('第'+str(i)+'页有'+str(len(divlist))+'个项目')
        if len(divlist)==0:
            print('爬取结束')
            return
        for div in divlist:
            a=div.find('a',class_='siteCardICH3')
            title=a.attrs['title'].replace(',','_')
            href=a.attrs['href']
            keylist=div.find('div',class_='siteCardFLabelBox siteIlB_box').find_all('a')
            keyValue=''
            for key in keylist:
                keyValue=keyValue+key.get_text()+'_'
            haveGet=div.find('div',class_='ftDiv').find('p',class_='ftP').get_text()
            support=div.find('div',class_='scDiv').find('p',class_='ftP').get_text()
            jindu=div.find('div',class_='thDiv').find('p',class_='ftP').get_text()
            row=[filename,title,href,keyValue,haveGet,support,jindu]
            # print(row)
            f1.write(str(row)+'\n')
            # csv_write.writerow(row)
# f1=open('zc_link.txt','w+',encoding='utf-8')

# getLink()
#存放失效链接
f3=open('error.txt','w+')
def getDetail(line):
    url=line[2]   
    bsObj=getObj(url)
    itemid=re.search(r'id-(.+?)$',url).group(1) 
    if bsObj==None:
        print(url)
        f3.write('url'+'\n')
        return
    try:
        target=bsObj.find('div',class_='xqRatioText clearfix').find('b').get_text()
    except:
        print(url)
        f3.write('url'+'\n')
        return
    sponsorid=bsObj.find('span',class_='txt2').get_text()
    concern=bsObj.find('div',class_='xqDetailLeft siteImgBox').find('a').get_text()
    
    clas=bsObj.find('span',class_='gy siteIlB_item').get_text()
    itemaddress=bsObj.find('span',class_='addr siteIlB_item').get_text()
    position=bsObj.find('span',class_='label siteIlB_item').get_text()
    refresh=bsObj.find('li',{'data-scrollto':'zxjzBox'}).find('b').get_text()
    comment=bsObj.find('li',{'data-scrollto':'plOuterBox'}).find('b').get_text()
    supportTime=bsObj.find('li',{'data-scrollto':'zczOuterBox'}).find('b').get_text()
    # try:
    #     footlist=bsObj.find('div',class_='zcjeOuterBox').find_all('div',class_='zcjeFooter')
    # except:
    #     print(url)
    #     f3.write('url'+'\n')
    #     return
    
    # l=len(footlist)
    # reTime=footlist[l-1].find_all('b')
    # reTime=reTime[len(reTime)-1].get_text()
    try:
        sponsor=bsObj.find('div',class_='item-contact item1').find_all('span')[-1].get_text()    
    except:
        sponsor=''
    
    try:
        address=bsObj.find('div',class_='item-contact item2').find_all('span')[-1].get_text()
    except:
        address=''
    try:
        phonenum=bsObj.find('div',class_='item-contact item3').find_all('span')[-1].get_text()
    except:
        phonenum=''
    row=[itemid,line[1],sponsorid,concern,line[-2],target,line[-3],line[-1],clas,itemaddress,position,refresh,comment,supportTime,sponsor,address,phonenum]
    csv_write2.writerow(row)
    try:
        refreshlist=bsObj.find('div',{'id':'progressList'}).find_all('div',class_='zxjz_NavItem')
        for div in refreshlist:
            time=div.find('p',class_='timeP').get_text()
            text=div.find('p',class_='textP').get_text()
            row=[itemid,time,text]        
            imglist=div.find('div',class_='picItem siteImgBox').find_all('img')
            for img in imglist:
                row.append(img.attrs['src'])
            csv_write18.writerow(row)
    except:
        pass
    maintext=bsObj.find('div',{'id':'xmxqBox'})
    text=maintext.get_text()
    row=['' for i in range(3)]
    row[0]=itemid
    row[1]=text
    try:
        videolist=maintext.find('div',class_='play-box') 
        src=videolist.find('img').attrs['src']
        row[2]='src'
    except:
        pass
    imglist=maintext.find_all('img')
    for img in imglist:
        row.append(img.attrs['src'])
    csv_write19.writerow(row)
    #评论
   

    # print(bsObj)
f4=open('error.txt','w+',encoding='utf-8') 
# header={
#     'Cookie':cook
# } 
def get_proxies_abuyun():
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"
    # 代理隧道验证信息
    proxyUser = 'HR3LY43V4QOU249D'
    proxyPass = 'F89DAEA7A6C85E23'

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
def getcomment(line):
    url=line[2]   
    itemid=re.search(r'id-(.+?)$',url).group(1) 
    j=0
    while True:
        # newUrl='http://www.zhongchou.cn/deal-support_list?id=748157&page_size=10&offset=20'
        newUrl='http://www.zhongchou.cn/deal-support_list?id='+itemid+'&page_size=10&offset='+str(j*10)
        # print(newUrl)
        for m in range(5):
            try:
                req=requests.get(newUrl,proxies=get_proxies_abuyun(),timeout=15)
                print(req.text)
                data=json.loads(req.text)['data']['support_list']

            except:
                time.sleep(3)
                pass
            if m==4:
                f4.write(newUrl+'\n')
                
                print(newUrl)
        for d in data:
            row=[itemid]+list(d.values())
            print(row)
            csv_write20.writerow(row)
            
        j=j+1
        if len(data)<10:
            break
        # time.sleep(3)


        


# f2=open(filename+'_final.csv','w+',encoding='gb18030',newline='')
# f18=open(filename+'_18.csv','w+',encoding='gb18030',newline='')
# f19=open(filename+'_19.csv','w+',encoding='gb18030',newline='')
f20=open(filename+'_支持记录.csv','w+',encoding='gb18030',newline='')
# f21=open(filename+'_21.csv','w+',encoding='gb18030',newline='')
# f22=open(filename+'_22.csv','w+',encoding='gb18030',newline='')
# f23=open(filename+'_23.csv','w+',encoding='gb18030',newline='')
# csv_write2=csv.writer(f2)
# csv_write18=csv.writer(f18)
# csv_write19=csv.writer(f19)
# csv_write20=csv.writer(f20)
# csv_write21=csv.writer(f21)
# csv_write22=csv.writer(f22)
# csv_write23=csv.writer(f23)
for line in csv.reader(open(filename+'.csv',encoding='gb18030')):
    # getDetail(line)
    getcomment(line)
    # break