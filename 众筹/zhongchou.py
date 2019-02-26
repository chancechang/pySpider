

from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
import time
import time
import json

# url='http://www.zhongchou.cn/browse/id-23-re-p'
# filename='公益'
# url='http://www.zhongchou.cn/browse/id-10007-re-p'
# filename='区块链'
# url='http://www.zhongchou.cn/browse/id-28-re-p'
# filename='农业'
# url='http://www.zhongchou.cn/browse/id-16-re-p'
# filename='出版'
# url='http://www.zhongchou.cn/browse/id-10001-re-p'
# filename='娱乐'
# url='http://www.zhongchou.cn/browse/id-22-re-p'
# filename='艺术'
url='http://www.zhongchou.cn/browse/id-18-re-p'
filename='其他'

def getLink():
    f1=open(filename+'.csv','w+',newline='',encoding='gb18030')
    csv_write=csv.writer(f1)
    for i in range(1,7):
        newurl=url+str(i)
        bsObj=mytemp.getObj(newurl).find('div',class_='sousuoListBox clearfix')
        divlist=bsObj.find_all('div',class_='ssCardItem')
        print(len(divlist))
        # return
        for div in divlist:
            a=div.find('a',class_='siteCardICH3')
            title=a.attrs['title'].replace(',','_')
            href=a.attrs['href']
            keylist=div.find('div',class_='siteCardFLabelBox siteIlB_box').find_all('a')
            keySum=len(keylist)
            haveGet=div.find('div',class_='ftDiv').find('p',class_='ftP').get_text()
            support=div.find('div',class_='scDiv').find('p',class_='ftP').get_text()
            jindu=div.find('div',class_='thDiv').find('p',class_='ftP').get_text()
            row=[filename,title,href,keySum,haveGet,support,jindu]
            print(row)
            csv_write.writerow(row)
        # print(bsObj)
getLink()
f3=open('error.txt','w+')
def getDetail(line):
    url=line[2]   
    bsObj=mytemp.getObj(url)
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
        
    concern=bsObj.find('div',class_='xqDetailLeft siteImgBox').find('a').get_text()
    refresh=bsObj.find('li',{'data-scrollto':'zxjzBox'}).find('b').get_text()
    comment=bsObj.find('li',{'data-scrollto':'plOuterBox'}).find('b').get_text()
    supportTime=bsObj.find('li',{'data-scrollto':'zczOuterBox'}).find('b').get_text()
    try:
        footlist=bsObj.find('div',class_='zcjeOuterBox').find_all('div',class_='zcjeFooter')
    except:
        print(url)
        f3.write('url'+'\n')
        return
    l=len(footlist)
    reTime=footlist[l-1].find_all('b')
    reTime=reTime[len(reTime)-1].get_text()
    if bsObj.find('div',{'id':'xmxqBox'}).find('img')!=None:
        pic='有'
    else:
        pic='无'
    if bsObj.find('div',class_='play-box')!=None:
        video='有'
    else:
        video='无'
        
    row=line+[target,concern,refresh,comment,supportTime,reTime,pic,video]
    print(row)
    csv_write2.writerow(row)
    # print(bsObj)
    
    


f2=open('公益'+'_final.csv','a+',encoding='gb18030',newline='')
csv_write2=csv.writer(f2)
for line in csv.reader(open(filename+'.csv',encoding='gb18030')):
    getDetail(line)
    # break