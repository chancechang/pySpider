import requests
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import xlwt
import time

cook='aliyungf_tc=AQAAAPNpCV8XiwIAO46cc1gU5UGt+5ga; __c=1521972816; W_CITY_S_V=53; AB_T=abvb; __g=-; Hm_lvt_1f6f005d03f3c4d854faec87a0bee48e=1521972826; __l=r=&l=%2Fgs.html%3Fka%3Dhead-com; isHasPushRecommentMessage=true; thirtyMinutes=true; isAutoOpenDialog=false; thirtyMinutesCount=4; __a=50032656.1521972816..1521972816.52.1.52.52; Hm_lpvt_1f6f005d03f3c4d854faec87a0bee48e=1521975040'
headers = {
    "Cookie":cook,
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

def phangetObj(url,f,crawl,city=None,indu=None,r=0):
    driver =webdriver.PhantomJS(executable_path="phantomjs.exe")   
    #使用浏览器请求页面
    driver.get(url)
    #加载3秒，等待所有数据加载完毕
    time.sleep(3)
    #通过id来定位元素，
    #.text获取元素的文本数据
    # dl=driver.find_elements_by_css_selector("#searchLeftOptions")
    pageSource=driver.page_source
    bsObj=BeautifulSoup(pageSource,"html.parser")
    if crawl.__name__=="firstcrawl":
        crawl(bsObj,f,city)
    else:
        crawl(bsObj,f,city,indu,r)   
    driver.close()

def getObj(url):
    req=None
    for i in range(5):
        try:
            req=requests.get(url,headers=headers,timeout=1000)
            req.encoding="utf-8"
            if req:
                break
        except:
            continue

    try:
        bsObj = BeautifulSoup(req.text,'html.parser')
    except AttributeError as e:
        return None
    return bsObj

def secondcrawl(bsObj,csv_write,city,indu,r):
    ul=bsObj.find("div",class_="wrap_style mt15").find("ul")
    lists=ul.find_all("li")
    for li in lists:
        smldiv=li.find("div")
        companyname=smldiv.find("a").get_text()
        p=smldiv.find("p").get_text().strip().split("|")
        smlindu=p[0]
        scale=""
        if len(p)>=3:
            scale=p[2]
        website=""
        if len(p)>=4:
            website=p[3]
        dds=li.find("dl").find_all("dd")
        score=dds[0].get_text().strip()
        salary=dds[1].get_text().strip().split("\xa0\xa0")[-1]
        row=[city,indu,companyname,smlindu,scale,website,score,salary]
        print(row)
        csv_write.writerow(row)
        # for i in range(0,len(row)):
        #     table.write(r,i,row[i])
        # r+=1

def firstcrawl(bsObj,f,city):
    dd=bsObj.find("dl",{"id":"searchLeftOptions"}).find("dd")
    lilists=dd.find_all("li")
    print(len(lilists))
    for li in lilists:
        a=li.find("a")
        industry=a.get_text()
        induhref=a.attrs["href"]
        f.write(str([city,industry,induhref])+"\n")
        
#深圳
#http://www.kanzhun.com/pla49p1.html?ka=select-condition-3
urls=["http://www.kanzhun.com/pla28p1.html","http://www.kanzhun.com/pla106p1.html"]
transfname="./data/industry1.txt"
def main(urls,transfname):
    f=open(transfname,"w" ,encoding="utf-8")
    for i in range(len(urls)):
        if i==0:
            city="东莞"
        else:
            city="厦门"
        phangetObj(urls[i],f,firstcrawl,city)
# main(urls,transfname)

def getlinks(filename):
    '''从txt文件中读取链接
    '''
    links=[]
    f=open(filename,encoding="utf-8")
    link=f.readline()
    while link:
        links.append(link.strip())
        link=f.readline()
    return links

global r 
translinks=getlinks(transfname)
for i in range(22,23):
    print(i)
    [city,indu,url]=eval(translinks[i])
    filename=city+"-"+indu.replace("/","_") 
    out=open("./data/"+filename+".csv","w+",encoding="gb18030",newline = '')
    csv_write=csv.writer(out)
    csv_write.writerow(["地区","行业领域","公司名称","行业","公司规模","网站","公司评分","月薪"])
    for j in range(1,11):                
        newurl="http://www.kanzhun.com"+url.replace("1.",str(j)+".")+"?ka=paging"+str(j)
        print(newurl)
        phangetObj(newurl,csv_write,secondcrawl,city,indu,(j-1)*10+1)
        
# for i in range(1,len(translinks)):
#     print(eval(translinks[i]))
#     [city,indu,url]=eval(translinks[i])
#     if i==1:
#         data=xlwt.Workbook()
#     if i==12:
#         data.save(city+".xls")
#         data=xlwt.Workbook()
#     if i==23:
#         data.save(city+".xls")
#         break
#     table=data.add_sheet(indu.replace("/","_"),cell_overwrite_ok=True)



        
