
from bs4 import BeautifulSoup
import requests
import xlsxwriter


cook='WebLogicSession=Z9ycfF0YzbYSiWUAFYw6PINgZbQurEQyCEuitU1yRA0LQTMBmcuv!-295674712; TS011e2724=01f90ab4d8619f228b08923ecd394e0f5521509d1c6df3fa676c0561bba50784a9ed7b413816da102bfe19668d86e1e6245984a2b0; www_iaqg_org_persist=479305934.47873.0000; TS01135089=01f90ab4d8ba923ea42896091b2408ec1a9cc77cb48933d1676fea6f10c7c9381dc11c565d4dcd312d899e864991dbd72ae820ce57'
cook='WebLogicSession=V32mtDWiUTIM3sbZa3rayij3giBqWAcivS1H-9JAa8dSLL0adc4U!-295674712; TS011e2724=01f90ab4d8b56171d90222b21b877842d10c5ea99cecb14b51a90cca3d972066391f4fc2f2f485a6e3314cbdd1cdaa8b827ea176e4; www_iaqg_org_persist=428974286.47873.0000; TS01135089=01f90ab4d897488241733e9731a7e48a82dc97a2c2829d05fa91d04fd0fe3c82ad6d940ceaa66cc160b0a145af14b14d056f7afe86'
header={
    'Cookie':cook,
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    # 'X-DevTools-Emulate-Network-Conditions-Client-Id':'(6E111686F4C1612F892FF0F1862152BE)'
}
def get_data():
    f=open('iaqg.txt','a+',encoding='utf-8',newline='')
    for i in range(392,415):
        print('第'+str(i)+'页')
        url='https://www.iaqg.org/oasis/csd!navigate?pg='+str(i)+'&isOverlay=1'
        req=requests.get(url,headers=header)
        bsObj=BeautifulSoup(req.text,'html.parser')
        div=bsObj.find('div',class_='tbl-container').find('tbody').find_all('tr')
        le=len(div)
        print(le)
        for j in range(le):
            oin=div[j].find('em',class_='ct-oin').get_text()
            name=div[j].find('div',class_='ct-org').find('strong').get_text()
            href=div[j].find('div',class_='ct-org').find('a').attrs['href']
            address=div[j].find('div',class_='ct-address').get_text()
            status=div[j].find('div',class_='tbl-2d-r mrkr-wrapped').get_text().replace('\n','').replace('\r','')
            Certified=div[j].find('div',class_='tbl-2d-r tbl-num').get_text().replace('\n','').replace('\r','')
            cert_num=div[j].find('div',class_='tbl-2d-r graceful-2d').get_text()
            CB=div[j].find('div',class_='tbl-2d-r tbl-2d-r-free token-right').get_text()
            struct=div[j].find_all('td')[-1].get_text().replace('\n','').replace('\r','')
            row=[oin,name,href,address,status,Certified,cert_num,CB,struct]
            print(row)
            f.write(str(row)+'\n')
    # print(row)
    # break
    f.close()
# get_data()
def write_xlsx():
    workbook = xlsxwriter.Workbook('iaqg_add_country.xlsx')     #创建工作簿
    sheet = workbook.add_worksheet()
    rowname=['oin','name','Location','country','Status','Standard','Cert Num','CB','Structure Type']
    r=0
    for i in range(len(rowname)):
            sheet.write(r,i,rowname[i])
    r=1
    for line in open('iaqg.txt','r',encoding='utf-8'):
        line=eval(line)
        line[7]=line[7].replace('\n','').replace('\r','')

        line=line[:2]+line[3:]
        country=line[2].split(',')[-1]
        line=line[:2]+[line[2].replace(','+country,''),country]+line[4:]
        for i in range(len(line)):
            sheet.write(r,i,line[i])
        r=r+1
    workbook.close()
write_xlsx()