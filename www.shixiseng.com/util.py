from bs4 import BeautifulSoup
import requests

def getObj(url,cook):
    headers = {
        "Cookie":cook,
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

    for i in range(5):
        try:
            html=requests.get(url,headers=headers)
            # html.encoding="utf-8"
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
