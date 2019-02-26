import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
import csv




def getObj(url,data):
    try:
        html=requests.post(url,data=data)
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

def crawl(bsObj,csv_write):
    divlist=bsObj.find_all('div',class_='comment_single')
    print(len(divlist))
    for div in divlist:
        style=div.find('span',class_='starlist').find('span').attrs['style']
        sty=style.split(';')
        for w in sty:
            wi=w.split(':')
            if wi[0]=='width':
                score=int(wi[1].replace("%",''))*5/100
                break
        comment=div.find('span',class_='heightbox').get_text()
        csv_write.writerow([comment,score])
        print(comment,score)

url='http://you.ctrip.com/destinationsite/TTDSecond/SharedView/AsynCommentView'
data=dict([('poiID','10558935'),
('districtId','152'),
('districtEName','Guangzhou'),
('pagenow',952),
('order',3.0),
('star',0.0),
('tourist',0.0),
('resourceId','48593'),
('resourcetype',2)])
f=open('ctrip.csv','a',newline='',encoding='gb18030')
csv_write=csv.writer(f)
# csv_write.writerow(['评论','评分'])
for i in range(952,1009):
    print('开始抓取第'+str(data['pagenow'])+'页评论') 
    bsObj=getObj(url,data)
    crawl(bsObj,csv_write)
    data['pagenow']+=1