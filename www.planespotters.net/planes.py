
# import openpyxl
# import xlrd
import requests
from bs4 import BeautifulSoup

# def write_to_txt():
#     mainData_book = xlrd.open_workbook("planes.xlsx")
#     mainData_sheet = mainData_book.sheet_by_index(0)
#     f=open('planes.txt','a+',encoding='utf-8')
#     for row in range(0, 45):
#         rowValues = mainData_sheet.row_values(row, start_colx=0, end_colx=2)
#         f.write(str(rowValues[0:2] )+'\n')
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
def get_obj(url):
    for i in range(5):
        try:
            req=requests.get(url,headers=header,proxies=get_proxies_abuyun(), timeout=15)
            req.encoding='utf-8'
            bsObj=BeautifulSoup(req.text,'html.parser')
            # print(bsObj)
            trlist=bsObj.find('table',class_='DataTable').find('tbody').find_all('tr')
            return trlist
        except:
            pass
    return None

header={
    'cookie':'__cfduid=da46aae8d274c008a451f65d51578af0b1543370877; __psuid=9771110c30682cf3136ec995e3e4d7f7; _ga=GA1.2.1651273487.1543370884; _gid=GA1.2.1190287158.1543370884; testSeed=417611948; cookieconsent_dismissed=true; PHPSESSID=472bq22nn3h88lbgrbbqlhkp5v; _pk_ses.1.9f6a=%2A; _pk_id.1.9f6a=914db19580a081eb.1543370877.34.1543377203..; _pk_cvar.1.9f6a=false',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}
# url='https://www.planespotters.net/production-list/Airbus/A220?p='+str(page)
f=open('planes_link.txt','w+',encoding='utf-8')
root='https://www.planespotters.net'
for line in open('planes.txt','r',encoding='utf-8'):
    line=eval(line)
    page=1
    print(line)
    lastrlist=''
    while True:
        url=line[1]+'?p='+str(page)
        # url='https://www.planespotters.net/production-list/Airbus/A220'+'?p='+str(page)
        trlist=get_obj(url)
        # print(trlist[0].find_all('td')[1].find('a').attrs['href'])
        if trlist[0]==lastrlist:
            print(str(page)+'  over')
            break
        lastrlist=trlist[0]        
        print(str(page)+' '+str(len(trlist)))
        for tr in trlist:
            tdlist=tr.find_all('td')
            # print(tdlist[1])
            row=line+[root+tdlist[1].find('a').attrs['href'],tdlist[2].get_text().replace('\n','')]
            # print(row)
            f.write(str(row)+'\n')
        page=page+1
        if page==3:
            break
        # break
    break

