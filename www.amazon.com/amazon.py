from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
import util

url='https://www.amazon.com/gp/bestsellers/'
# cook='x-wl-uid=1dHco/VSrJUr16cnal2zhX6vpptnf4AZhcNa/loYAgQ+NsTX74UP3GaGl0clmH3emUWIHs090zfY=; session-id-time=2082787201l; session-id=134-3004528-9385933; ubid-main=132-1824970-6094049; session-token=mUNaFyPCLT56ljnF/PF0NMpsPHmbzk8zALIuu2fSSFzi6KlE0liX1gy6aizYplJ/dzb+7L2rl8PIvaoyfJmu77/v87IJ8ZznR7Dyokn7vgezwuk0o/MhmR4vyP9zDFDPr7uFyAt6hc3aq5gpfXl1BBN8mbEMHR+1xE3vSoy9Ii09aOsI3Az3CYSIhztxL9UzsMxfNFxW5ZF8BeSjaRLYL6LlKsb0DkZSRL3XnyHa8V5dZ1s9Yap9vRUJqKQLUhU8z6jtAb/FpQ4=; csm-hit=tb:4RNZBNMQ5NGHVEEG8FGR+b-4RNZBNMQ5NGHVEEG8FGR|1537281999632&adb:adblk_no'
# header={
#     ":authority":"www.amazon.com",
#     ":method":"GET",
#     ":path":"/gp/bestsellers/",
#     ":scheme":"https",
#     "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     "accept-encoding":"gzip, deflate, br",
#     "accept-language":"zh-CN,zh;q=0.9",
#     "cache-control":"max-age=0",
#     "cookie":"x-wl-uid=1dHco/VSrJUr16cnal2zhX6vpptnf4AZhcNa/loYAgQ+NsTX74UP3GaGl0clmH3emUWIHs090zfY=; session-id-time=2082787201l; session-id=134-3004528-9385933; ubid-main=132-1824970-6094049; session-token=mUNaFyPCLT56ljnF/PF0NMpsPHmbzk8zALIuu2fSSFzi6KlE0liX1gy6aizYplJ/dzb+7L2rl8PIvaoyfJmu77/v87IJ8ZznR7Dyokn7vgezwuk0o/MhmR4vyP9zDFDPr7uFyAt6hc3aq5gpfXl1BBN8mbEMHR+1xE3vSoy9Ii09aOsI3Az3CYSIhztxL9UzsMxfNFxW5ZF8BeSjaRLYL6LlKsb0DkZSRL3XnyHa8V5dZ1s9Yap9vRUJqKQLUhU8z6jtAb/FpQ4=; csm-hit=tb:4RNZBNMQ5NGHVEEG8FGR+b-4RNZBNMQ5NGHVEEG8FGR|1537281999632&adb:adblk_no",
#     "upgrade-insecure-requests":"1",
#     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
# }
header={
    'Host': 'www.amazon.com', 
    'Referer': 'https://www.amazon.com', 
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

}
def getObj(url,proxyIs=False,header=None,encode='utf-8'):
    for i in range(5):
        try:
           
            if proxyIs==False:
                html=requests.get(url,headers=header)
            else:
                html=util.build_proxy_request(url)
            html.encoding=encode  
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
bsObj=getObj(url,True,header)
print(bsObj)
lilist=bsObj.find('ul',{'id':'zg_browseRoot'}).find_all('li')
for li in lilist:
    url=li.find('a').attrs['href']
    print(url)

