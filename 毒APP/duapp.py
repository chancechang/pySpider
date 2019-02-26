
from bs4 import BeautifulSoup
import requests
import csv
import sys
sys.path.append("..")
import mytemp
import util
import urllib.request
import urllib3
import json

# d-c-left view-phone-wrapper
# /search/list?size=[]&title=&typeId=0&catId=2&unionId=0&sortType=0&sortMode=1&page=0&limit=20&sign=4b86e534b0d233207a435111f61f8247
# []&title=&typeId=0&catId=2&unionId=0&sortType=0&sortMode=1&page=2&limit=20&sign=e485ae8eddd95547a0271beda45d09d5 
url2='https://du.hupu.com/search/list?size=[]&title=&typeId=0&catId=2&unionId=0&sortType=0&sortMode=1&page=2&limit=20&sign=e485ae8eddd95547a0271beda45d09d5'
# url2='https://du.hupu.com/search/list?size=[]&title=&typeId=0&catId=2&unionId=0&sortType=0&sortMode=1&page=0&limit=20&sign=4b86e534b0d233207a435111f61f8247'
# /search/list?size=[]&title=&typeId=0&catId=4&unionId=0&sortType=0&sortMode=1&page=0&limit=20&sign=4cdb522927a504aea797cca21dac7109
# /search/list?size=[]&title=&typeId=0&catId=3&unionId=0&sortType=0&sortMode=1&page=0&limit=20&sign=bfa5ef97196795f488cd2f31a178e6c3
cook='duToken=d41d8cd9%7C15144277%7C1537232477%7C471d784cc1d9f4d0'
headers = {
    "Cookie":cook,
    "User-Agent":"duapp/3.4.3(android;5.1)",
    "Accept":"gzip",
    "duchannel": "opp",
    "dudeviceTrait":"", 
    "duloginToken": "1ae353c3|15144277|970656557f5309bb",
    "duplatform": "android",
    "duuuid": "fbc5ea1f51716822",
    "duv": "3.4.3",
    "Connection": "Keep-Alive",
    "Host": "du.hupu.com"
    }

def getJson(url,data,cook):
    #获取json
    urllib3.disable_warnings()
    f= requests.get(url,headers=headers,verify=False)
    print(f.text)
    try:
        target=json.loads(f.text)['data']['productList']
        for tar in target:
            print(tar)
            break
    except:
        pass
    # html=urllib.request.urlopen(f).read().decode('utf-8',"ignore")
    # #post方法请求json数据
    # r = requests.post(url, data = data)
    # target=''
    # try:
    #     target=json.loads(r.text)#["BusinessHallList"]  
    #     print(target)
    # except:
    #     pass
    return None
getJson(url2,None,cook)
