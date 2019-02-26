from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
import time

# url_root1='http://bj.to8to.com/company/list_'
cook='uid=CgoKUFuKdF6kME+yDXKiAg==; pt_219ae376=uid=UdDl79koxU8W0qvMuuyWUw&nid=1&vid=i1DpOAF0gkluLvVFUtAFXg&vn=1&pvn=1&sact=1538795291516&to_flag=0&pl=CvdYKJBkDejdzyIeS5a-EQ*pt*1538795291516; pt_s_219ae376=vt=1538795291516&cad=; to8to_landpage=https%3A//www.to8to.com/yezhu/; to8to_landtime=1538795291; to8tocookieid=38d4493d7a33a475fbc85ba79da0a51b962721; to8to_cook=OkOcClPzRWV8ZFJlCIF4Ag==; Hm_lvt_dbdd94468cf0ef471455c47f380f58d2=1538795292; city_from_ip=æ­¦æ±; sourcepath=b4%7Cb4; com_pop_flag=true; to8to_sourcepage=http%3A//sz.to8to.com/company/; tender_popup_flag=true; visitPage=true; to8tosessionid=s_225b33fabfdab187949143a571ffad1c; to8to_townid=1672; to8to_tcode=bj; to8to_tname=%E5%8C%97%E4%BA%AC; ONEAPM_BI_sessionid=9049.905|1538797704801; page-num=2; to8to_nowpage=http%253A%252F%252Fbj.to8to.com%252Fcompany%252F; Hm_lpvt_dbdd94468cf0ef471455c47f380f58d2=1538797795; act=freshen'


def getdetail():
    f1=open('company.csv','w+',encoding='gb18030',newline='')
    csv_write1=csv.writer(f1)
    for line in csv.reader(open('city.csv','r',encoding='gb18030')):
        time.sleep(3)
        city_name=line[0]
        print(city_name)
        if city_name=='昆明':
            continue
        url_root1=line[1]+'company/list_'
        i=1
        while True:
            print(i)
            url=url_root1+str(i)+'.html'
            bsObj=mytemp.getObj(url,False,cook)
            div1=bsObj.find('div',class_='xgt_meitu_searchNone')
            if div1!=None:
                break
                
            div=bsObj.find('div',class_='default__company__list')
            try:
                lilist=div.find_all('li',class_='company-data ')
            except:
                
                print([city_name,i])
                break
            # print(len(lilist))
            for li in lilist:
                # print(li)
                href=li.find('a').attrs['href']
                phone=''
                try:
                    phone=li.find('p',class_='company__phone').get_text().strip()
                except:
                    pass
                name=li.find('p',class_='company__name').find('span',class_='name').get_text().strip()
                row=[city_name,name,phone,href]
                print(row)
                csv_write1.writerow(row)
            i=i+1
getdetail()

def getcity():
    f2=open('city.csv','w+',encoding='gb18030',newline='')
    csv_write2=csv.writer(f2)
    url='http://www.to8to.com/index.html'
    bsObj=mytemp.getObj(url,False,cook)
    divbox=bsObj.find('div',{'id':'city_box'})
    citybox=divbox.find_all('div',class_='cs_zs')
    for box in citybox:
        print(box)
        citylist=box.find('div',class_='xzcs_dt').find_all('a')
        for city in citylist:
            href=city.attrs['href']
            cityname=city.get_text().strip()
            row=[cityname,href]
            print(row)
            csv_write2.writerow(row)
# getcity()

    
            



