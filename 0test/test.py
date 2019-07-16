from bs4 import BeautifulSoup
import requests
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
import time
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
import re
from email.mime.text import MIMEText
import smtplib #python 内置函数，无需安装
import urllib
from urllib.request import quote, unquote


def txt_to_excel(excelname,txtname):
    j=1
    workbook = xlsxwriter.Workbook(excelname+str(j)+'.xlsx') #创建工作簿
    sheet = workbook.add_worksheet()
    r=0
    for line in open(txtname+'.txt','r',encoding='utf-8'):
        line=eval(line)
        if r==60000:
            workbook.close()
            j=j+1
            workbook = xlsxwriter.Workbook(excelname+str(j)+'.xlsx') #创建工作簿
            sheet = workbook.add_worksheet()
            r=0
        for m in range(len(line)):
            sheet.write(r,m,line[m])
        r=r+1       
    workbook.close()
# txt_to_excel()

def get_proxies_abuyun():
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"
    # 代理隧道验证信息
    proxyUser = 'HR3LY43V4QOU249D'
    proxyPass = 'F89DAEA7A6C85E23'

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies



def sendmsg(msg,from_addr,password,to_addr):
    # 输入SMTP服务器地址:
    smtp_server = 'smtp.qq.com'  #163邮箱为'smtp.163.com'
    server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()    

def test_email():
    from_addr = '85386227@qq.com'
    # from_addr = '1509662199@qq.com'

    password = 'qzlqxznqbzbcbhbj'
    # password = 'chang222701'
    to_addr = '1509662199@qq.com'
    msg = MIMEText('this is a test', 'plain', 'utf-8')
    sendmsg(msg,from_addr,password,to_addr)
cook='UM_distinctid=16a49bfa276317-0593895cd86b63-12376d51-13c680-16a49bfa27731a; Hm_lvt_dd5339bc2fb909694c2ddf9a84a97be0=1556015457; Hm_lvt_908e530051baf6bf8f1099623d31e59c=1556015457; gr_user_id=82ae14e0-0932-4522-b070-afc4c13794e1; browerSupportTipShowed=true; mediav=%7B%22eid%22%3A%2248256%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22ZW%3A2a(sLnH%3Ai%5D5Y(%2F%24SN%22%2C%22ctn%22%3A%22%22%7D; gdxidpyhxdE=IUPsJI6%2BP73RYoM2c86ao986UMl5pvrBWEpD0BdE4314fM1vYsoYJLYTZjGd0lQPuqbVqLwstjAYo6DfjlCOYh%2FQB8gR1PPgibP4t7VsJdwuQ7XSTlSwJx9UL4yaHyIiw1kCNQhiDOChLe6x5v5a7i79nTy2yE0xz8RbVQMH%2BvNjptsW%3A1556018035665; _9755xjdesxxd_=32; registerType=personal; lg_=lge8KYX93S; id=d3374f30-1da2-47e9-bfec-ae7eebb6d131; Qs_lvt_61680=1556015457%2C1556071180; JSESSIONID=95B1CE3DDB57E9DB8CDC360641869496; CNZZDATA1273697089=334151955-1556013910-%7C1556074104; Hm_lpvt_dd5339bc2fb909694c2ddf9a84a97be0=1556075296; Qs_pv_61680=3281641669470619600%2C4095147902753979000%2C883016162210597600%2C207171821202568350%2C1261160359973022500; __xsptplus799=799.3.1556073652.1556075296.23%234%7C%7C%7C%7C%7C%23%23_UM8qxyTiHnTWS0tkGmqJgQ7ui-Iieq7%23; Hm_lpvt_908e530051baf6bf8f1099623d31e59c=1556075296; _sp_id_.30b0=0a43d22e-d3a8-4739-92f9-21d970da6433.1556015458.3.1556075296.1556071237.b5cc2787-7377-4f32-8ad7-d295045a4440.null'
cook='ASP.NET_SessionId=t3nmpx3pkda45q5lm1qhot4x; Hm_lvt_0d4eb179db6174f7994d97d77594484e=1556113143; Hm_lpvt_0d4eb179db6174f7994d97d77594484e=1556113436'
req_header = {'Cookie':cook,
    "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    'X-Requested-With': 'XMLHttpRequest'
    }
url='http://k3.fanmugua.net/Home/Detail?NovelId=4053&novelTitleNo=9&referralId='
# http://k3.fanmugua.net/Home/Detail?NovelId=4053&novelTitleNo=4&referralId=
url='https://www.vipmro.com/?ticket=63a1dd97-89c7-414b-810c-e70784f27bd3'
url='https://www.vipmro.com/ss/c-541110'
url='https://www.vipmro.com/product/1618525'


# req=requests.get(url,headers=req_header,proxies=get_proxies_abuyun() )
# bsObj=BeautifulSoup(req.text,'html.parser')
# # div=bsObj.find('div',class_='m-category-children')
# # div=bsObj.find('div',class_='list-main J_emptyGood')
# div=bsObj.find('table',class_='product-pros topper')
# div=bsObj.find('table',class_='product-pros m-top20')
# div=bsObj.find('table',class_='detail-attrs-right-attrs J_attrs')

url='https://www.zydmall.com/dsvr/product/searcher.ashx?do=list'
data={
    'key': 'null',
    'ncata_id': "44",
    'page_index': 1,
    'page_size': "60",
    'sbrand_names': [],
    'sort': "",
    'specs': [],
    'sprop_names': [],
}
div=requests.post(url,headers=req_header,data=json.dumps(data))



print(div.text)