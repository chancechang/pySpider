# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 09:37:14 2018

@author: 李畅
"""

from bs4 import BeautifulSoup
import requests

cook='Hm_lvt_8b3e2b14eff57d444737b5e71d065e72=1532134364; jobui_p=1532134364592_63781463; PHPSESSID=ancv7b2271e7af3n5ec9m5d4f6; jobui_area=%25E5%25B9%25BF%25E5%25B7%259E; TN_VisitCookie=8; TN_VisitNum=8; Hm_lpvt_8b3e2b14eff57d444737b5e71d065e72=1532135574'

headers = {
    "Cookie":cook,
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
def getObj(url):
    for i in range(5):
        try:
            html=requests.get(url,headers=headers)
            html.encoding="utf-8"
            break
        except HTTPError as e:
            # time.sleep(3)
            print('再次请求')
            print('HTTPError')
            return None
    try:
        bsObj = BeautifulSoup(html.text,'html.parser')
    except AttributeError as e:
        print('AttributeError')
        return None
    return bsObj
root1='https://www.jobui.com/cmp?keyword=%E6%B7%B1%E5%9C%B3%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&area=%E5%85%A8%E5%9B%BD&n='
root2='#listInter'

obj=getObj(root1+str(1)+root2)
print(obj)

