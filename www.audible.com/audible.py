from bs4 import BeautifulSoup
import requests
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
import time
import json
import xlsxwriter
import re

def phangetObj(url):
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

    return pageSource


cook='ubid-main=132-8719085-8034119; session-id=131-5873086-3324150; session-id-time=2082787201l; originalSourceCode="ANONAUDW0378WS010202_11/24/2018 14:12"; isFirstVisit=false; AMCVS_165958B4533AEE5B0A490D45%40AdobeOrg=1; check=true; AAMC_audible_0=REGION%7C11; aam_uuid=64062401540651915390981476480203761960; _fbp=fb.1.1543068754793.2023467469; x-main="D4x4DOvJ1bjC5PS3l2cQi@ugXnzQeDiN@vW@e0KVsnY@LB2CCgtPhV2tSeq@jKcA"; at-main=Atza|IwEBIFfsrMiL8KtOlN8-s4nHgnGji7uA3fq0paMQ2gc1piAPE8b9RzQ_KgFTFGi_NAj4G5im4r-SU4yGHOjeD0YQDB5WAhR4FBQbrr4hU2UstvBBlvMXPFhqt089dyie4MWtgujZ-8t5tcg-4oAEajGGYT-WKWm-9XC77E1jM6SKB6I2Tj1FCpz-jPftUrMnPvRS1OtvzEo0Vh0KAZFatK2v-u-kUr9o-c9S2jCFqRzdjIkQdWOdupmIW7Drqw6oWk71-TX4-XYzCzg7lbeizLWtPElnM7nboj1XVvYLG6BR1lNDPqhOfx3JFVNoZH2jEw4PO6rXI3il44X0sTf0Gp2krA9QfnD8OLFLN1n7DDFvvh1yD6qU9FoJD4xhuH3NOM_JawxIH_hXJndUC3N2ZBpnFvjP; userType=amzn; session-token="YZySc/pkv1uYpt1Z1kfx1R6fimx23p2Xh3izC6f+v04J3PXnUgSoaL9z8FAVw/SfuzbAC7E+zejuDgXUdy3IrEA6O7JmFEvTE7juVlLZZpzyIQHu1ZgLwH3JYmASUSsDGK2v1W8JPQssZV+mDoV8bWjXuiOISne1ncAgwQAjbGDoY/428qZj5Q3j115lmRXzkpoW3Gv0ho48THokhiYqBA=="; currentSourceCode="ANONAUDW0378WS010202_11/24/2018 14:17"; s_sq=%5B%5BB%5D%5D; AMCV_165958B4533AEE5B0A490D45%40AdobeOrg=-330454231%7CMCIDTS%7C17860%7CMCMID%7C64083647032229527780979105674863908881%7CMCAAMLH-1543674101%7C11%7CMCAAMB-1543674101%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1543075949s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.2%7CMCCIDH%7C2095516621; mbox=session#fbc09480b6234200a1320354df2add20#1543071162|PC#fbc09480b6234200a1320354df2add20.22_41#1606313553; csm-hit=tb:KJJ8JZZ80GJW293A646S+s-ZS7AR0XG6QPM4MYVA3RT|1543069536792&adb:adblk_no; s_sess=%20s_cc%3Dtrue%3B%20s_ppvl%3Dadbl-best-sellers%252C11%252C3%252C650%252C1366%252C150%252C1366%252C768%252C1%252CP%3B%20s_ppv%3Dadbl-best-sellers%252C100%252C8%252C5909%252C1366%252C175%252C1366%252C768%252C1%252CP%3B; s_pers=%20gpv_pn%3Dadbl-best-sellers%7C1543071895736%3B%20s_getNewRepeat%3D1543070095744-New%7C1545662095744%3B%20s_lv%3D1543070095748%7C1637678095748%3B%20s_lv_s%3DFirst%2520Visit%7C1543071895748%3B'
header={
    'Cookie':cook,
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'referer':'www.audible.com',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Referer':'https://www.audible.com/adblbestsellers?ref=a_adblbests_l1_catRefs_1&pf_rd_p=a30c7ab3-6e06-4708-af2f-e103a849b3b1&pf_rd_r=892K6Y9ASPMY5VV22MFM&&searchCategory=2226646011'
}
def get_data():
    f=open('audible.txt','a+',encoding='utf-8')
    for i in range(200,203):
        print(i)
    # url='https://www.audible.com/search?ref=a_search_c4_pageSize_3&pf_rd_p=1d79b443-2f1d-43a3-b1dc-31a2cd242566&pf_rd_r=WP15VX2TE5Y4HTRVSZ6M&&submitted=1&sort=review-rank&pageSize=50'
        # url='https://www.audible.com/search?ref=a_search_c4_pageNum_1&pf_rd_p=1d79b443-2f1d-43a3-b1dc-31a2cd242566&pf_rd_r=JCWN416546VC7K2ZXW4Y&&submitted=1&sort=review-rank&pageSize=50&page='+str(i)
        url='https://www.audible.com/search?ref=a_search_c1_sort_5&pf_rd_p=073d8370-97e5-4b7b-be04-aa06cf22d7dd&pf_rd_r=CBG2VT6C8DJDDMR9C4JC&&submitted=1&sort=review-rank&pageSize=50&page='+str(i)
        # req=requests.get(url,headers=header)
        req=phangetObj(url)
        # print(req)
        div=BeautifulSoup(req,'html.parser').find('div',{'id':'center-3'})
        lilist=div.find_all('li',class_='bc-list-item productListItem')

        for j in lilist:
            text=str(j.find_all('div',class_='bc-col-12')[2])
            text=re.sub('[\n]+',' ',text)
            f.write(str(text)+'\n')
            # print(i.
        # print(li)
        print(len(lilist))
    f.close()

def get_format():
    f=open('audible_data.txt','w+',encoding='utf-8')

    r=0
    rowName=['title','By','Narrated by','Series','Length','Release date','stars','ratings']
    for t in open('audible.txt','r',encoding='utf-8'):
        line=BeautifulSoup(t,'html.parser')
        lilist=line.find_all('li',class_='bc-list-item')
        le=len(lilist)
        row=['' for i in range(8)]
        for j in range(len(lilist)):
            li=lilist[j]
            text=li.get_text()
            text=re.sub('[ ]+',' ',text).strip()
            if j==0:
                row[0]=text
                continue
            for r in range(1,len(rowName)):
                if rowName[r] in text:
                    if r==6:
                        row[r]=text.split('out of')[0]
                        row[r+1]=text.split('stars')[1].replace(',','').replace('ratings','')
                    else:
                        row[r]=text
                    break
        f.write(str(row)+'\n')
        print(row)
            # print(text+'\n')
        # break
        r=r+1
    print(r)

rowName=['title','By','Narrated by','Series','Length','Release date','stars','ratings']

workbook=xlsxwriter.Workbook('audible_total.xlsx')
sheet=workbook.add_worksheet()
r=0
for i in range(8):
    sheet.write(r,i,rowName[i])
for line in open('audible_data.txt','r',encoding='utf-8'):
    line=eval(line)
    # if line[7]!='' and int(line[7])>8000:
    r=r+1
    for i in range(8):
        sheet.write(r,i,line[i])
print(r)
workbook.close()
