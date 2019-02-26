
from bs4 import BeautifulSoup
import requests
import time
import datetime
import json
import re
import xlsxwriter
import os



cook='shshshfpa=3716a4c3-457c-62f8-3984-99f57985b0f8-1530629113; shshshfpb=1a6d428e2eadd4007a5d510cf3fa35763247552e8427356e25b3b8bfc7; 3AB9D23F7A4B3C9B=C4PWX5Z5AY5Y5DTJHKUEQML5EMPZARRPMBEYK2XJF4LMNILKOB4SXWE6MNFXFNEX6DGW427AJ2WHU6PFBYQTADGW7A; shshshfp=a9830361b9d79ed805599f95367fbf8b; qd_uid=JRUE89TM-1J73RPYXKKTDYXJW0LLS; qd_fs=1549530126771; sec_flag=3e3987f6857ee5f6b918504d735e0507; sec_addr=c0a80168; recentbrowse=402946108da9480c88d1f6bb5161df12; _ga=GA1.3.1440352996.1549530229; _gid=GA1.3.1181634154.1549530229; __jdv=238784459|direct|-|none|-|1549542321640; __jdu=1549542321635273379847; __jdc=238784459; _pcd_=809ca791e87180b4b2ef81e928277e35; ordDeviceType=pc; ordAppCode=6; ordSystemType=pc; qd_ad=-%7C-%7Cdirect%7C-%7C0; qd_ls=1549542322130; qd_ts=1549544647764; qd_sq=2; qd_sid=JRUE89TM-1J73RPYXKKTDYXJW0LLS-2; __jda=238784459.1549542321635273379847.1549542322.1549542322.1549544648.2; __jdb=238784459.1.1549542321635273379847|2.1549544648; _jrda=2; _jrdb=1549544649004'
header={
    'Cookie':cook,
    'origin':'https://z.jd.com',
    'referer':'https://z.jd.com/bigger/search.html',
    'cache-control':'max-age=0',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
}
#种植技术
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

def get_z_jd_link():
    
    f=open('z_jd_link1.txt','w+',encoding='utf-8')
    
    for i in range(1,100):
        print('第'+str(i)+'页')
        url='https://z.jd.com/bigger/search.html'
        data={
            # 'productEnd':-28,
            'page':i,
            # 'status':'8',
            # 'sort':'zhtj'
        }
        # ,proxies=get_proxies_abuyun()
        req=requests.post(url,data,headers=header)
        req.encoding='utf-8'
        bsObj=BeautifulSoup(req.text,'html.parser')
        jshu=bsObj.find_all('li',class_='info type_now')
        jshu1=bsObj.find_all('li',class_='info type_xm')

        print(len(jshu))
        print(len(jshu1))
        
        for div in jshu:
            if div.find('li',class_='fore3').find('p',class_='p-percent').get_text()=='0天':
                #写入
                a=div.find('a')
                h4=div.find('h4',class_='link-tit')
                get=div.find('li',class_='fore1').find('p',class_='p-percent').get_text()
                money=div.find('li',class_='fore2').find('p',class_='p-percent').get_text()
                # div.find('li',class_='fore3')
                f.write(str([a.attrs['href'],h4.attrs['title'],get,money])+'\n')
        # break
    f.close()

# get_z_jd_link()


def get_Obj(line,f_error):
    url='https://z.jd.com'+line[0]
    print(url)
    for i in range(5):
        try:
            req=requests.get(url,headers=header)
            bsObj=BeautifulSoup(req.text,'html.parser')
            support=bsObj.find('p',class_='p-progress').find('span',class_='fr').get_text()
            return bsObj
        except:
            pass
        if i == 4:
            f_error.write(str(line)+'\n')
            print(url+'失效')
    return None

# f=open('z_jd_detail.txt','a+',encoding='utf-8')
# f_error=open('z_jd_error.txt','a+',encoding='utf-8')

# for line in open('z_jd_link.txt','r',encoding='utf-8'):
#     line=eval(line)
#     bsObj=get_Obj(line,f_error)
#     # money=bsObj.find('p',class_='p-num').get_text()
#     support=bsObj.find('p',class_='p-progress').find('span',class_='fr').get_text()
#     redlist=bsObj.find('p',{'id':'projectMessage'}).find_all('span',class_='f_red')
#     for red in redlist:
#         if '￥' in red.get_text():
#             target=red.get_text()
#     # focus=bsObj.find('a',{'id':'a_focus'})
#     # focus=bsObj.find('span',{'id':'focusCount'}).get_text()
#     # prais=bsObj.find('span',{'id':'praisCount'}).get_text()
#     processor_name=bsObj.find('div',class_='promoters-name').find('span',class_='fl').get_text().replace('\t','').replace('\r','').replace('\n','').strip()
#     num=bsObj.find('div',class_='promoters-num').find('span',class_='num').get_text()
#     addresslist=bsObj.find('ul',class_='contact-box').find_all('li',class_='clearfix contact-li')
#     address=''
#     for addr in addresslist:
#         if '地址' in  addr.get_text():
#             address=addr.get_text()
#             break
#     row=line+[support,target,processor_name,num,address]
#     # print(row)
#     # break
#     f.write(str(row)+'\n')
# f.close()

# f=open('z_jd_final.txt','w+',encoding='utf-8')
# for line in open('z_jd_detail.txt','r',encoding='utf-8'):
#     line=eval(line)
#     header={
#         'Referer':'https://z.jd.com'+line[0],
#         'Host':'sq.jr.jd.com',
#         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
#     }
#     print(line[0])
#     id=line[0].replace('/project/details/','').replace('.html','')
#     url='https://sq.jr.jd.com/cm/getCount?key=1000&systemId='+id
#     req=requests.get(url,headers=header)
#     # print(req.text)
#     text=req.text.replace('(','').replace(')','')
#     js=json.loads(text)['data']
#     focus=js['focus']
#     prais=js['praise']
#     row=line+[focus,prais]
#     f.write(str(row)+'\n')
#     # print(row)
# f.close()

workbook = xlsxwriter.Workbook('京东金融.xlsx') #创建工作簿
sheet = workbook.add_worksheet()
r=0
for line in open('z_jd_final.txt','r',encoding='utf-8'):
    line=eval(line)
    for m in range(len(line)):
        sheet.write(r,m,line[m])
    r=r+1 
workbook.close()
