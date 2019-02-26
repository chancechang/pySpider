from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
import time
import json

data={
    'session_key':'774334640@qq.com',
    'session_password':'774334640a',
# session_redirect:/voyager/loginRedirect.html
}
# loginUrl='https://www.linkedin.com/uas/login-submit'
# response=requests.post(loginUrl,data)
# print(response.text)
cook='''
tgw_l7_route=76a155b56fddae6480ecdc917ed8e1bf; 
PHPSESSID=b15846k01brrb997s9n0chv5h7; username=xingwd%40hlsushi.com.cn; uin=332; 
skey=65bc17cfa44da5146b86845e27a1867465a7ce9b84af5b28; exp=316000; username=xingwd@hlsushi.com.cn'''
header={
    # 'Referer':'http://wx.bilalipay.com/_components/user/login.html?jump=http%3A%2F%2Fwx.bilalipay.com%2Fmember%2Findex%2Findex',
    'Cookie':cook,
    'X-Requested-With':'XMLHttpRequest'
}
# header['X-Requested-With']='XMLHttpRequest'

url='''http://wx.bilalipay.com/index.php?r=member/record/user&g_tk=1493447614&storename=all&starttime=2
018-10-10+23%3A02%3A01&endtime=2018-10-17+23%3A02%3A01&sort=&card=4&page=1&_=1539788522582'''
req=requests.get(url,headers=header)
print(req.text)