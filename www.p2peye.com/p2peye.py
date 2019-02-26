import urllib.request
import json
from bs4 import BeautifulSoup
import requests
import csv
import time
from threading import Thread

cook='A4gK_987c_saltkey=UcaccK0Y; A4gK_987c_lastvisit=1522494722; TYID=enANiFq/exI0SX37DCRxAg==; __jsluid=7195481c128d19fd955e259ef9b33fa0; A4gK_987c_sendmail=1; bdp_data_is_new_user=true; __firstReferrerKey__=%7B%22%24first_referrer%22%3A%22%22%2C%22%24first_referrer_host%22%3A%22%22%7D; bdp_data2017jssdkcross=%7B%22distinct_id%22%3A%221627bf8e28410b-0541aef3d2eba7-b353461-1049088-1627bf8e28518d%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22user_id%22%3A%22a6yzmE3V%22%2C%22%24is_first_session%22%3A1%7D%7D; Hm_lvt_556481319fcc744485a7d4122cb86ca7=1522498347; Hm_lpvt_556481319fcc744485a7d4122cb86ca7=1522498347; __bdpa_session_key__2017__=%7B%22session_time%22%3A1522498366610%2C%22session_id%22%3A%221627bf8e28e333-069708e40079e2-b353461-1049088-1627bf8e29066f%22%2C%22session_hasBeenExpired%22%3A0%2C%22lastSend_sessonId%22%3A%221627bf8e28e333-069708e40079e2-b353461-1049088-1627bf8e29066f%22%7D; A4gK_987c_lastact=1522498404%09platformData.php%09issue'
headers = {
    "Cookie":cook,
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

def getObj(url):
    req=None
    for i in range(5):
        try:
            req=requests.get(url,headers=headers,timeout=1000)
            req.encoding="gbk"
            if req:
                break
        except:
            continue

    try:
        bsObj = BeautifulSoup(req.text,'html.parser')
    except AttributeError as e:
        return None
    return bsObj


def getJson(url):
    #获取json
    f= urllib.request.Request(url,headers=headers)
    html=urllib.request.urlopen(f).read().decode('utf-8',"ignore")
    data = json.loads(html)["data"]  
    return data

def crawl(url,filename):   
    f=open(filename,"w" ,encoding="utf-8")

    for i in range(1,203):
        try:
            data=getJson(url+str(i))
            print("正在爬取第"+str(i)+"页")
        except:
            print(str(i)+"出错")
            time.sleep(3)
            crawl(url,filename)
            break
        for i in range(len(data)):
            info=data[i]
            name=info['name']
            black_time=info['black_time']
            city_name=info['city_name']
            online_time=info['online_time']
            black_url=info['black_url']
            black_type_name=info['black_type_name']
            f.write(str([black_time,name,city_name,online_time,black_type_name,black_url])+"\n")
            # print(black_time,name,city_name,online_time,black_type_name,black_url)


def getlinks(filename):
    '''从txt文件中读取内容
    '''
    links=[]
    f=open(filename,encoding="utf-8")
    link=f.readline()
    while link:
        links.append(link.strip())
        link=f.readline()
    return links


def detailcrawl(url,detail,csv_write):
    infolist=["" for i in range(7)]
    try:
        bsObj=getObj(url)
        trlist=bsObj.find('table',class_='t_table').find_all('tr')
    except:
        csv_write.writerow(detail)
        print(url+'不可用')
        print(detail)
        return
    for i in range(len(trlist)):
        if trlist[i].find_all('td')[0].get_text().strip()=='注册资本':
            infolist[0]=trlist[i].find_all('td')[1].get_text()
        elif trlist[i].find_all('td')[0].get_text().strip()=='法人':
            infolist[1]=trlist[i].find_all('td')[1].get_text()
        elif trlist[i].find_all('td')[0].get_text().strip()=='风险暴露时间':
            infolist[2]=trlist[i].find_all('td')[1].get_text()
        elif trlist[i].find_all('td')[0].get_text().strip()=='注册人数':
            infolist[3]=trlist[i].find_all('td')[1].get_text()
        elif trlist[i].find_all('td')[0].get_text().strip()=='募集资金':
            infolist[4]=trlist[i].find_all('td')[1].get_text()
        elif trlist[i].find_all('td')[0].get_text().strip()=='待收金额':
            infolist[5]=trlist[i].find_all('td')[1].get_text()
        elif trlist[i].find_all('td')[0].get_text().strip()=='现状':
            infolist[6]=trlist[i].find_all('td')[1].get_text()      

    print(detail+infolist)
    csv_write.writerow(detail+infolist)
    return 
 
class my_thread(Thread):
    def run(self):
        detailcrawl(self.href,self.detail,self.csv_write)
    def __init__(self,href,detail,csv_write):
        Thread.__init__(self)
        self.href=href
        self.detail=detail
        self.csv_write=csv_write 


filename='p2peye.txt'
url='https://www.p2peye.com/platformData.php?mod=issue&ajax=1&action=getPage&page='
crawl(url,filename)
#读取
rows=getlinks(filename)
#写入
csv_write=csv.writer(open('p2peyefinal.csv','w+',encoding='gb18030',newline=''))
csv_write.writerow(["问题发生时间","平台名称","所在地区","上线时间","出问题原因","url","注册资本","法人","风险暴露时间","注册人数","筹集资金","待收金额","现状"])

ThreadList=[]
for j in range(0,len(rows)):
    detail=eval(rows[j])
    newurl=detail[5]
    t=my_thread(newurl,detail,csv_write)
    ThreadList.append(t)
    t.start()
for t in ThreadList:
    t.join()