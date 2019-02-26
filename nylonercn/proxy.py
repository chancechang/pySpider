from bs4 import BeautifulSoup
import requests
from urllib.error import HTTPError
import hashlib
import base64
import time
import json
#涉及到动态加载，加密，Cookie反爬，IP频率限制
cook='sessionid=ly7xq9pffl7awndyo8opyynx5l96giyz'
headers = {
    "Cookie":cook,
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

def getObj(url):
    for i in range(5):
        try:
            html=requests.get(url,headers=headers)
            html.encoding="gbk"
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

def md5hashlib(s):
    m=hashlib.md5()
    m.update(s.encode('utf-8'))
    return (m.hexdigest())


def decode_str(scHZjLUh1):   
#   解密    
#   scHZjLUh1 = Base64["\x64\x65\x63\x6f\x64\x65"](scHZjLUh1);
    scHZjLUh1 = base64.decodestring(scHZjLUh1)
    key=b'nyloner' 
    lenth= len(key)
    schlenth=len(scHZjLUh1)
    code=''
    for i in range(schlenth):
        coeFYlqUm2 = i % lenth
        code+= chr(scHZjLUh1[i] ^ key[coeFYlqUm2])
    code = base64.decodestring(code.encode())
    iplist = code.decode()
    return (iplist)

def get_proxy_ip():
    #页码从1开始
    for i in range(1,100):
        timestamp=int(time.time())
        page=i
        token = md5hashlib(str(page) + str(15) + str(timestamp))
        url='https://nyloner.cn/proxy?page=' + str(page) + '&num=15' + '&token=' + token + '&t=' + str(timestamp)
        Obj=getObj(url)
        print(json.loads(Obj.text))
        # data=bytes(json.loads(Obj.text)['list'],encoding='utf8')
        # data=json.loads(decode_str(data))
        # if len(data)<15:
        #     break
        # print('第'+str(page)+'页')
        # for d in data:
        #     print(d)



# print(md5hashlib('a'))
while True:
    get_proxy_ip()
    time.sleep(10)