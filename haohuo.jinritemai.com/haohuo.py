
from bs4 import BeautifulSoup
import requests
url='https://item.jd.com/13165121126.html'

url='https://haohuo.jinritemai.com/views/product/item?id=3298686377922791332'
# cook='shshshfpa=3716a4c3-457c-62f8-3984-99f57985b0f8-1530629113; shshshfpb=1a6d428e2eadd4007a5d510cf3fa35763247552e8427356e25b3b8bfc7; ipLoc-djd=1-72-2799-0; user-key=6a64c93c-2f4b-4508-85b8-8491aa571d52; cn=0; 3AB9D23F7A4B3C9B=C4PWX5Z5AY5Y5DTJHKUEQML5EMPZARRPMBEYK2XJF4LMNILKOB4SXWE6MNFXFNEX6DGW427AJ2WHU6PFBYQTADGW7A; __jdu=1530629094966642932306; shshshfp=a9830361b9d79ed805599f95367fbf8b; shshshsID=9bb7c3cc62700b42f936c426af6cb347_1_1542529569971; __jda=122270672.1530629094966642932306.1530629095.1540186310.1542529570.5; __jdb=122270672.1.1530629094966642932306|5.1542529570; __jdc=122270672; __jdv=122270672|direct|-|none|-|1542529570426'
cook='_tea=TEA-8f9ddc88-f0bf-b4e2-d280-9d6ac43d9812; seed.js%3Asession=%7B%22id%22%3A%221672abc4013433-0ad9b4d665f517-b353461-100200-1672abc401c15c%22%2C%22page%22%3A%221672abc401f81d-0e900dfba3d74e-b353461-100200-1672abc40246ee%22%2C%22created%22%3A1542610239527%7D'
header={
    # 'X-Requested-With':'XMLHttpRequest',  
    'Cookie':cook,
    # 'if-none-match':'W/"5bee8df8-4d60"'
    # 'Host':'item.jd.com',
    # 'Upgrade-Insecure-Requests':'1',
    # 'Referer':'https://search.jd.com/search?keyword=%E8%8C%B6%E5%8F%B6&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E8%8C%B6%E5%8F%B6&cid2=12202&cid3=12203&page=9&s=197&click=0',
    # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
}
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
url='https://haohuo.snssdk.com/product/ajaxstaticitem?id=3298686377922791332'
html=requests.get(url,proxies=get_proxies_abuyun())
print(html.text)
# bsObj=BeautifulSoup(html.text,'html.parser')
# print(bsObj)