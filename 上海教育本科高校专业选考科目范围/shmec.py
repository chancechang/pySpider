import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
import csv
import math
import re
from threading import Thread

cook='ant_stream_59df58828c697=1521631012/3280484770; bow_stream_59df58828c697=13; _gscu_1601713973=21602093xhf89o98; _gscbrs_1601713973=1; _gscs_1601713973=21602093sq4q4498|pv:3'
headers = {
    "Cookie":cook,
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

def getObj(url):
    try:
        html=requests.get(url,headers=headers)
        html.encoding="gb2312"
    except HTTPError as e:
        print('HTTPError')
        return None
    try:
        bsObj = BeautifulSoup(html.text,'html.parser')
    except AttributeError as e:
        print('AttributeError')
        return None
    return bsObj

def detailcrawl(region,title,url):
    newbsObj=getObj(url)
    trList=newbsObj.find("div",{"id":"ivs_content"}).find_all("tr")
    if trList[0].find_all("td")[1].get_text().strip()=="专业方向":
        print(url+"  特殊处理1")
        for m in range(1,len(trList)):
            tdList=trList[m].find_all("td")
            if len(tdList)==3:
                major1=tdList[0].get_text().strip()
                major2=tdList[1].get_text().strip()
            else:
                major2=tdList[0].get_text().strip()
            subjects=tdList[-1].get_text().strip()
            major=major1+" "+major2
            if subjects=="不作要求" or subjects=="不限" or subjects=="无" or subjects=="无选考科目"  :
                subjectnum=0
            else:
                subjectnum=max(subjects.count("、"),subjects.count(" "),subjects.count("，"),subjects.count("  "))+1
            remark=""
            csv_write.writerow([region,title,major,subjectnum,subjects,remark])           
        return
    # if trList[0].find_all("td")[0].get_text().strip().replace("\n","")=="专业（类）代码":
    #     print(url+"  特殊处理2")
    #     for m in range(1,len(trList)):
    #         tdList=trList[m].find_all("td")
    #         major=tdList[1].get_text().strip()                       
    #         if len(tdList)>=3:
    #             subjects=tdList[2].get_text().strip()
    #         if len(tdList)==4:
    #             remark=tdList[3].get_text().strip()
    #         if subjects=="不作要求" or subjects=="不限" or subjects=="无" or subjects=="无选考科目"  :
    #             subjectnum=0
    #         else:
    #             subjectnum=max(subjects.count("、"),subjects.count(" "),subjects.count("，"),subjects.count("  "))+1
    #         csv_write.writerow([region,title,major,subjectnum,subjects,remark])           
    #     return

    # for m in range(1,len(trList)):
    #     tdList=trList[m].find_all("td")
    #     major=tdList[1].get_text().strip()      
    #     subjects=tdList[2].get_text().strip()
    #     if subjects=="不作要求" or subjects=="不限" or subjects=="无" or subjects=="无选考科目"  :
    #         subjectnum=0
    #     else:
    #         subjectnum=max(subjects.count("、"),subjects.count(" "),subjects.count("，"),subjects.count("  "))+1
    #     remark=tdList[3].get_text().strip()
    #     csv_write.writerow([region,title,major,subjectnum,subjects,remark])           
    # return
        
    remark=""
    for i in range(1,len(trList)):
        tdList=trList[i].find_all("td")
        if len(tdList)==1:
            continue
        major=tdList[0].get_text().strip()      
        subjects=tdList[1].get_text().strip()
        if subjects=="不作要求" or subjects=="不限" or subjects=="无" or subjects=="无选考科目"  :
            subjectnum=0
        else:
            subjects=re.sub(' +', ' ', subjects)
            subjectnum=max(subjects.count("、"),subjects.count(" "),subjects.count("，"),subjects.count("  "))+1
        if len(tdList)>=3:
            remark=tdList[2].get_text().strip()        
        if "rowspan" in tdList[0].attrs and tdList[0].attrs["rowspan"]=="2":
            if "rowspan" in tdList[1].attrs and tdList[1].attrs["rowspan"]=="2":
                remark=remark+trList[i+1].get_text()
        # print([region,title,major,subjectnum,subjects,remark])
        csv_write.writerow([region,title,major,subjectnum,subjects,remark])
        
def crawl(href,region):
    n=1
    url="http://www.shmec.gov.cn/web/jyzt/xkkm2017/{}&page={}".format(href,str(n))
    bsObj=getObj(url).find("div",{"id":"content"})
    ul=bsObj.find("ul",class_="ul02")
    if ul.get_text().strip()=="":
        print("选考科目表未上报或正在考核中")
        csv_write.writerow([region,"选考科目表未上报或正在考核中"])
    else:
        max=int(bsObj.find("div",class_="xyy").find_all("font",{"color":"red"})[-1].get_text())
        while n<=max:
            liList=ul.find_all("li")
            for li in liList:
                try:
                    a=li.find("a")
                    title=a.attrs["title"]
                    newhref=a.attrs["href"]
                except AttributeError as e:
                    print('AttributeError')
                    return None
                print(title,newhref)                  
                detailcrawl(region,title,"http://www.shmec.gov.cn/web/jyzt/xkkm2017/"+newhref)
            n=n+1
            url="http://www.shmec.gov.cn/web/jyzt/xkkm2017/{}&page={}".format(href,str(n))
            ul=getObj(url).find("div",{"id":"content"}).find("ul",class_="ul02")

class my_thread(Thread):
    def run(self):
        crawl(self.href,self.region)
    def __init__(self,href,region):
        Thread.__init__(self)
        self.href=href
        self.region=region


out=open('shmec1.csv', 'w+',encoding='gb18030',newline = '')
csv_write=csv.writer(out)

mainList=getObj("http://www.shmec.gov.cn/web/jyzt/xkkm2017/index.php?").find("div",{"id":"leftcolumn"}).find_all("li")
ThreadList=[]
for j in range(30,len(mainList)):
    li=mainList[j]
    print(li.a.attrs["href"])
    print(li.get_text())
    t=my_thread(li.a.attrs["href"],li.get_text())
    ThreadList.append(t)
    t.start()
    # break
for t in ThreadList:
    t.join()







# crawl(3318)
# detailcrawl("湖北","三峡大学","http://www.shmec.gov.cn/web/jyzt/xkkm2017/detail.php?article_id=79380&area_id=3303")

# html=requests.get("http://www.shmec.gov.cn/web/jyzt/xkkm2017/index.php?area_id=3288&page=1",headers=headers)
# print(html)
# bsObj = BeautifulSoup(html.text,'html.parser').find("div",{"id":"content"}).find("ul",class_="ul02")
# # .find("ul",class_="ul02")
# print(bsObj)