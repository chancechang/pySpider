
from bs4 import BeautifulSoup
import requests
import csv
import sys
import time
import util

urlRoot='http://www.mafengwo.cn/yj/10444/2-0-'
# cookie='PHPSESSID=d8jjork1sdfla03t5vfn708qr6; mfw_uuid=5b728c09-93ad-8541-b9a7-d4f44bf3b2a8; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222018-08-14+16%3A00%3A09%22%3B%7D; uva=s%3A78%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1534233610%3Bs%3A10%3A%22last_refer%22%3Bs%3A6%3A%22direct%22%3Bs%3A5%3A%22rhost%22%3Bs%3A0%3A%22%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1534233610%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A0%3A%22%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5b728c09-93ad-8541-b9a7-d4f44bf3b2a8; UM_distinctid=1653773178143-08ac53b7b6bf12-b353461-100200-165377317823a2; CNZZDATA30065558=cnzz_eid%3D442987233-1534231255-%26ntime%3D1534236655; __mfwlv=1534241055; __mfwvn=2; __mfwlt=1534241138'

def main1():
    f=open('qdtime.csv','w+',newline='',encoding='gb18030')
    csv_write=csv.writer(f)
    #708
    for i in range(0,720):
        newUrl=urlRoot+str(i)+'.html'
        # print('正在爬取第'+str(i)+'页...')
        for i in range(5):
            try:
                html=util.build_proxy_request(newUrl)
                obj = BeautifulSoup(html.text,'html.parser')
                lilist=obj.find('div',class_='post-list').find_all('li',class_='post-item clearfix')
                break
            except:
                # print('第'+str(i)+'次尝试')
                if i==4:
                    print('没找到'+newUrl)
                # time.sleep(5)

        # obj = BeautifulSoup(html.text,'html.parser')
        # lilist=obj.find('div',class_='post-list').find_all('li',class_='post-item clearfix')
        print(len(lilist))
        for li in lilist:
            a=li.find('h2').find_all('a')[-1]
            time=li.find('span',class_='comment-date').get_text().split(' ')[0]
            if 'href' not in  a.attrs:
                print('position error')
            else:
                wr=[a['href'],time]
                # print(wr)
                csv_write.writerow(wr)

main1()