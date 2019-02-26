


from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
import time
import json

cook='_ga=GA1.2.1703842908.1540366194; _gid=GA1.2.938428636.1540366194; __rtgt_sid=jnmu9dyvq6npjl; d7s_uid=jnmu9dyvq6npjl; __gads=ID=c35de3e961f66749:T=1540366196:S=ALNI_MY3mzcz1VfRuGML50nsDHTPItCx_A; __qca=P0-604528955-1540366226275; d7s_spc=3; _ceg.s=ph3epl; _ceg.u=ph3epl'
# Referer:https://zh.flightaware.com/live/flight/ABL391/history/20180801/1245Z/RKPK/VHHH/tracklog

url='https://zh.flightaware.com/live/flight/ABL391/history/20180801/1245Z/RKPK/VHHH/tracklog'

header={
    'Cookie':cook,
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    'Upgrade-Insecure-Requests':"1",
    'Host':'zh.flightaware.com',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    # 'Referer':'http://m.qichacha.com/firm_2923c76a374d1fb8c5700d2a5c34ef68.html'
    # 'Referer':'http://sfq.ahqi.gov.cn/demoQuery/list?pageNow=2&demoCode=&demoName=&assumeUnit=&cityId=0&productId=&demoBatch=&mgrMode=&demoLevel=&beginYear='
}


# url='http://m.qichacha.com/firm_2923c76a374d1fb8c5700d2a5c34ef68.html'
# url='https://www.qichacha.com/g_CQ.html'
    # http://m.qichacha.com/firm_2923c76a374d1fb8c5700d2a5c34ef68.html
bsObj=requests.get(url,headers=header)
# bsObj=requests.get(url,headers=header)
bsObj=BeautifulSoup(bsObj.text,'html.parser')

# bsObj=mytemp.getObj(url,False,cook)
tr=bsObj.find_all('tr',class_='smallrow1')[20]
print(str(tr))