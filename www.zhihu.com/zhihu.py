
import urllib.request 
import requests
from bs4 import BeautifulSoup
import csv
import json
from urllib.error import HTTPError
import sys
sys.path.append("..")
import mytemp
import util

cook='_zap=103062c2-b140-4bb3-9b09-c6cf339bb388; d_c0="AECCyMfSwQyPTpKO0aCmkPUGPKluXFgq_Bw=|1511945695"; __DAYU_PP=EbUEJqyeeFNufYfVivYR2ba2111a3034; _xsrf=342e908a-93bd-4e26-bb31-ee4cb0e42acb; q_c1=deb5f34c9c784ae5b70a9cae0b24ee5d|1521542185000|1501208857000; capsion_ticket="2|1:0|10:1521558824|14:capsion_ticket|44:MjEwZjI4NTI4Mjk2NGRkZWFiMWZjY2JjY2I3Mjk0NjA=|629b05c7a8cb266f450ffe58788e2c07e56051bdcc00b7957f702bd49017e4c5"; z_c0="2|1:0|10:1521558888|4:z_c0|92:Mi4xdDlrX0FnQUFBQUFBUUlMSXg5TEJEQ1lBQUFCZ0FsVk5hSE9lV3dCaHRfdnRXbnYzc3FiRGdFZUpBMW1CcmstUFZ3|f3cebdebc483f14d2bab9d9f4048d79bd5f77237fe51453a66c2a90d8bf8d54d"; unlock_ticket="ABCK5wre8ggmAAAAYAJVTXAssVpzFDh0uhrcnxHvYPpchsYSmNRR_g=="'
cook='_zap=103062c2-b140-4bb3-9b09-c6cf339bb388; d_c0="AECCyMfSwQyPTpKO0aCmkPUGPKluXFgq_Bw=|1511945695"; __DAYU_PP=EbUEJqyeeFNufYfVivYR2ba2111a3034; __utma=155987696.981327916.1523262016.1523262016.1523262016.1; q_c1=deb5f34c9c784ae5b70a9cae0b24ee5d|1526914520000|1501208857000; tgw_l7_route=7139e401481ef2f46ce98b22af4f4bed; _xsrf=3af145ab-c18c-406b-a784-d025e77c0315'
headers = {
    "Cookie":cook,
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

out=open('zhihuUser1.csv', 'w+',encoding='gb18030',newline = '')
csv_write=csv.writer(out)

def getObj(url):
    try:
        html=requests.get(url,proxies=util.get_proxies_abuyun())
    except HTTPError as e:
        print('HTTPError')
        return None
    try:
        bsObj = BeautifulSoup(html.text,'html.parser')
    except AttributeError as e:
        print('AttributeError')
        return None
    return bsObj
   
def crawl(username,url):
    #提取链接中people和following之间的用户标识
    Id=url.split("/")[-2] 
    # print(Id)
    #获取网页解析
    bsObj=getObj(url)
    #判定该用户是否关注别人
    if bsObj.find("div",class_='EmptyState'):
        print("该用户未关注任何人")
        csv_write.writerow([username,url,None,None])
    else:
        i=0
        newUrl="http://www.zhihu.com/api/v4/members/"+Id+"/followees?include=data%5B%2A%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset="+str(i)
        print(newUrl)
        #获取json
        # proxy = urllib.request.ProxyHandler(util.get_proxies_abuyun())
        # opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        # urllib.request.install_opener(opener)

        # f= urllib.request.Request(newUrl,headers=headers)
        html=requests.get(newUrl,headers=headers,proxies=util.get_proxies_abuyun() )
        html=html.text
        # print(html)
        # .decode('utf-8',"ignore")
        
        try:
            data = json.loads(html)["data"]  
        except:
            print(html)
            if html==None:
                raise Error           
        while data:
            print("第"+str(i/10)+"页")
            for d in data:
                csv_write.writerow([username,url,d["name"],d["url"]])
                print(d["name"],d["url"])
            i=i+20
            newUrl="http://www.zhihu.com/api/v4/members/"+Id+"/followees?include=data%5B%2A%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset="+str(i)
            f= urllib.request.Request(newUrl,headers=headers)
            html=urllib.request.urlopen(f).read().decode('utf-8',"ignore")
            data = json.loads(html)["data"] 

#csv文件的读取
csv_reader = csv.reader(open('sample.csv', encoding='gb18030'))
for row in csv_reader:
    username=row[0]
    url=row[1]
    print(row[1])
    crawl(username,url)
    
# crawl("123","https://www.zhihu.com/people/kuang-wu-87-8/following")

# html=urllib.request.urlopen("https://www.zhihu.com/people/xbjf/following")
# # print(html)
# bsObj = BeautifulSoup(html,'html.parser').find("div",{"id":"Profile-following"})
# # .find("div",{"id":"Profile-following"})
# print(bsObj)