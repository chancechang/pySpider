import requests
from bs4 import BeautifulSoup
 
url = "http://www.v2ex.com/signin"
UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"
 
header = { "User-Agent" : UA,
           "Referer": "http://www.v2ex.com/signin"
           }
 
v2ex_session = requests.Session()
f = v2ex_session.get(url,headers=header)
 
soup = BeautifulSoup(f.content,"html.parser")
once = soup.find('input',{'name':'once'})['value']
print(once)
 
postData = { 'u': 'whatbeg',
             'p': '*****',
             'once': once,
             'next': '/'
             }
 
v2ex_session.post(url,
                  data = postData,
                  headers = header)
 
f = v2ex_session.get('http://www.v2ex.com/settings',headers=header)
print(f.content.decode())