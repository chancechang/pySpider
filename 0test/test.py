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
def phangetObj(url):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
    )
    dcap["phantomjs.page.settings.cookie"] = (
    header['Cookie']
    )

    driver =webdriver.PhantomJS(executable_path="phantomjs.exe",desired_capabilities=dcap)   
    #使用浏览器请求页面
    driver.get(url)
    #加载3秒，等待所有数据加载完毕
    time.sleep(3)
    #通过id来定位元素，
    #.text获取元素的文本数据
    # dl=driver.find_elements_by_css_selector("#searchLeftOptions")
    # dl=driver.find_element_by_id("searchLeftOptions")
    # dl.click()
    pageSource=driver.page_source

    return pageSource
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


url='https://apimobile.meituan.com/group/v4/poi/pcsearch/107?uuid=4d50f4dc3b988b807423.1539736060.1.0.0&userid=-1&limit=32&offset=64&cateId=-1&q=%E6%97%85%E6%B8%B8%E6%99%AF%E7%82%B9'
cook='_lxsdk_cuid=1667f6baf91c8-04f7ddad48d3f9-b353461-100200-1667f6baf91c8; uuid=4d50f4dc3b988b807423.1539736060.1.0.0; cityname=%E6%AD%A6%E6%B1%89; iuuid=7DF7B105F41F28DFB2E6A60539BFF902268DC021C5C083524829D94165F5A3A4; webp=1; _lxsdk=7DF7B105F41F28DFB2E6A60539BFF902268DC021C5C083524829D94165F5A3A4; ci=107; rvct=107; _lxsdk_s=168885868a7-f15-510-d26%7C%7C33'
header={
    'Cookie':cook,
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    # 'X-DevTools-Emulate-Network-Conditions-Client-Id':'(6E111686F4C1612F892FF0F1862152BE)'
}

req=requests.get(url,headers=header)
print(req.text)



 
