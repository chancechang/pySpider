import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
import time

url='https://yun.baidu.com/s/1c2N43Uo'
url='https://yun.baidu.com/s/1i5ox9Rn'
# cook='BIDUPSID=66631E8806F253074D257F98459F243B; PSTM=1504097369; MCITY=-218%3A; BAIDUID=8789992A98CF1EEFEDC917B0F4BE592C:FG=1; BDSFRCVID=Ya8sJeCCxG3ZO3R7dtoxOwLDg-eupC8urNue3J; H_BDCLCKID_SF=tJ-t_CKXfCvbfP0khtQtbtCs5UPX5-CsBG6dQhcH0hOWsIOLXTbCjP08MxOKWM5kBtj-L4JnfP5K845NDUC0D6v0jH_8q6nfb5kXWRjD5RrJfnAk-PI3WtobKP6-3MJO3b7z2KO4JbbMDPnO5UvUbIu85q3mqnQHBjT-ohFLK-oj-DLxjTjP; H_PS_PSSID=1422_21085_27244; delPer=0; PSINO=1; BDRCVFR[Fc9oatPmwxn]=srT4swvGNE6uzdhUL68mv3; PANWEB=1; recommendTime=guanjia2018-11-16%2012%3A15%3A00'
cook='BIDUPSID=AF8BE128F17DACBFDB1071DCBB300F03; PSTM=1508300082; FP_UID=efad604e38bd92e886e3106324895355; BAIDUID=D1AC7AF720E266B578DD76A28B13B1DF:FG=1; pgv_pvi=9686739968'
header={
    'Cookie':cook,
    'Host':'yun.baidu.com',
    # Upgrade-Insecure-Requests:1
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}

driver =webdriver.PhantomJS()   
#使用浏览器请求页面
driver.get(url)
# driver.add_cookie(header)
#加载3秒，等待所有数据加载完毕
time.sleep(3)


# req=requests.get(url,headers=header)
# req.encoding='utf-8'
pageSource=driver.page_source

bsObj=BeautifulSoup(pageSource,'html.parser')
# print(bsObj)
print(bsObj.find_all('h2',class_='file-name'))