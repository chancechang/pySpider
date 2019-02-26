
from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
from selenium import webdriver
import time

def phangetObj(url,data=None):
    driver =webdriver.PhantomJS(executable_path="phantomjs.exe")   
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
    bsObj=BeautifulSoup(pageSource,"html.parser")
    driver.close()
    return bsObj

# url='https://club.jd.com/comment/productCommentSummaries.action?referenceIds=10198901480,580716,5810165,5315247&_=1540174845827'
# url='https://club.jd.com/comment/productCommentSummaries.action?referenceIds=8797196,1000486727,11814942529,10113059838&callback=jQuery7385036&_=1540179109400'
url='https://search.jd.com/s_new.php?keyword=%E8%8C%B6%E5%8F%B6&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E8%8C%B6%E5%8F%B6&cid2=12202&cid3=12203&stock=1&page=3&s=57&click=0'
# urlroot='https://search.jd.com/search?keyword=%E8%8C%B6%E5%8F%B6&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E8%8C%B6%E5%8F%B6&cid2=12202&cid3=12203&page='
f=open('jd3.csv','w+',encoding='gb18030',newline='')
csv_write=csv.writer(f)
cook='__jdu=1530629094966642932306; shshshfpa=3716a4c3-457c-62f8-3984-99f57985b0f8-1530629113; shshshfpb=1a6d428e2eadd4007a5d510cf3fa35763247552e8427356e25b3b8bfc7; __jdv=122270672|direct|-|none|-|1540174372745; __jdc=122270672; PCSYCityID=1381; xtest=1297.cf6b6759; ipLoc-djd=1-72-2799-0; rkv=V0800; 3AB9D23F7A4B3C9B=C4PWX5Z5AY5Y5DTJHKUEQML5EMPZARRPMBEYK2XJF4LMNILKOB4SXWE6MNFXFNEX6DGW427AJ2WHU6PFBYQTADGW7A; qrsc=3; _gcl_au=1.1.445880751.1540175146; shshshfp=0f80bc9836f30e768f7f992deb969bfd; user-key=6a64c93c-2f4b-4508-85b8-8491aa571d52; cn=0; __jda=122270672.1530629094966642932306.1530629095.1540174373.1540178883.3; __jdb=122270672.2.1530629094966642932306|3.1540178883; shshshsID=53c39878d8429a2479bdc1c0ebc9f431_2_1540179322671'
header={
    'X-Requested-With':'XMLHttpRequest',  
    'Cookie':cook  ,
    'Host':'search.jd.com',
    'Referer':'https://search.jd.com/search?keyword=%E8%8C%B6%E5%8F%B6&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E8%8C%B6%E5%8F%B6&cid2=12202&cid3=12203&page=9&s=197&click=0',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
}
m=0
def main():
    for i  in range(19,41,2):
        print(i)
        url=urlroot+str(i)
        bsObj=phangetObj(url)
        lilist=bsObj.find('div',{'id':'J_goodsList'}).find_all('li')
        print(len(lilist))
        for li in lilist:
            try:
                div=li.find('div',class_='p-name p-name-type-2')
                title=div.get_text()
                href=div.find('a').attrs['href']
                row=[title,href]
                print(row)
                csv_write.writerow(row)
            except:
                pass


# bsObj=mytemp.getObj(url,False,cook,'utf-8')
url='https://item.jd.com/13165121126.html'
cook='shshshfpa=3716a4c3-457c-62f8-3984-99f57985b0f8-1530629113; shshshfpb=1a6d428e2eadd4007a5d510cf3fa35763247552e8427356e25b3b8bfc7; ipLoc-djd=1-72-2799-0; user-key=6a64c93c-2f4b-4508-85b8-8491aa571d52; cn=0; 3AB9D23F7A4B3C9B=C4PWX5Z5AY5Y5DTJHKUEQML5EMPZARRPMBEYK2XJF4LMNILKOB4SXWE6MNFXFNEX6DGW427AJ2WHU6PFBYQTADGW7A; __jdu=1530629094966642932306; shshshfp=a9830361b9d79ed805599f95367fbf8b; shshshsID=9bb7c3cc62700b42f936c426af6cb347_1_1542529569971; __jda=122270672.1530629094966642932306.1530629095.1540186310.1542529570.5; __jdb=122270672.1.1530629094966642932306|5.1542529570; __jdc=122270672; __jdv=122270672|direct|-|none|-|1542529570426'
header={
    # 'X-Requested-With':'XMLHttpRequest',  
    'Cookie':cook,
    # 'Host':'item.jd.com',
    'Upgrade-Insecure-Requests':'1',
    # 'Referer':'https://search.jd.com/search?keyword=%E8%8C%B6%E5%8F%B6&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E8%8C%B6%E5%8F%B6&cid2=12202&cid3=12203&page=9&s=197&click=0',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
}


html=requests.get(url,headers=header)
bsObj=BeautifulSoup(html.text,'html.parser')
print(bsObj)

# print(bsObj)
# f.write(str(bsObj))

# url='https://item.jd.com/13165121126.html'

# 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv13782&productId=13165121126&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
# #评论信息
# 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=13165121126&callback=jQuery6385795&_=1540175728147'
# bsObj=mytemp.getObj(url).find('div',class_='p-parameter')
# bsObj=mytemp.getObj(url).find('div',class_='Ptable-item')

# # f=open('jd1.txt','w+',encoding='gb18030')
# print(str(bsObj.text))
