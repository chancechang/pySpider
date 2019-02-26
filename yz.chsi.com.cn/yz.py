import xlrd
from bs4 import BeautifulSoup
import requests
import time
import csv
import datetime
import json
import re
import xlsxwriter
import os
import xlrd
from concurrent.futures import ThreadPoolExecutor



cook='JSESSIONID=4A107305FE5EB708768A644A848ED003; acw_tc=2760825015468300558364418e3eba9bf96948bdefc768fe12e7da23de4722; _ga=GA1.4.1809379773.1546830059; _gid=GA1.4.1420037155.1546830059'
header={
    'Cookie':cook,
    'Host':'yz.chsi.com.cn',
    'Referer':'https://yz.chsi.com.cn/zsml/queryAction.do',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
}

data={
    'mldm':'03',
    'yjxkdm':'0301',
    'pageno':'2'
}

# 
# 
# print(req.text)

def two(i):
    if i <10:
        return '0'+str(i)
    else:
        return str(i)

#拿到所有编码
# 
# for i in range(2,14):   
#     row=['zyxw',two(i)+'5']
#     data['mldm']=row[0]
#     for j in range(1,10):
#         data['yjxkdm']=row[1]+str(j)
#         #开始循环页码
#         for k in range(1,100):
#             data['pageno']=k
#             req=requests.post(url,data=data,headers=header)
#             bsObj=BeautifulSoup(req.text,'html.parser')

def get_code():
    f=open('code.txt','a+',encoding='utf-8')
    url='https://yz.chsi.com.cn/zsml/pages/getMl.jsp'
    #学科类别

    req=requests.post(url,data={},headers=header)
    print(req.text)
    js=json.loads(req.text)

    url1='https://yz.chsi.com.cn/zsml/pages/getZy.jsp'
    req1=requests.post(url1,data={'mldm':''},headers=header)
    print(req1.text)
    jk=json.loads(req1.text)

    for j in js:
        for k in jk:
            if k['dm'][:2]==j['dm']:
                row=[j['dm'],k['dm'],j['mc'],k['mc']]
                print(row)
                f.write(str(row)+'\n')
    f.close()

def get_link_two():
    url='https://yz.chsi.com.cn/zsml/queryAction.do'
    f1=open('link_one.txt','a+',encoding='utf-8')
    for line in open('code.txt','r',encoding='utf-8'):
        line=eval(line)
        data['mldm']=line[0]
        data['yjxkdm']=line[1]
        print(line[:2])
        last_one=''
        for i in range(1,100):
            print(i)
            data['pageno']=str(i)
            req=requests.post(url,data=data,headers=header)
            bsObj=BeautifulSoup(req.text,'html.parser')
            div=bsObj.find('div',class_='zsml-list-box').find('table',class_='ch-table').find('tbody').find_all('tr')
            if last_one==div[0].find_all('td')[0].get_text():
                break
            if '抱歉' in div[0].find_all('td')[0].get_text():
                print('无数据')
                break

            for tr in div:
                row=line[2:4]
                td_list=tr.find_all('td')
                row.append(td_list[0].get_text().replace('\n',''))
                row.append(td_list[0].find('a').attrs['href'])
                row.append(td_list[1].get_text())
                row.append(td_list[2].get_text())
                for m in range(3,6):
                    if td_list[m].find('i')==None:
                        row.append('否')
                    else:
                        row.append('是')
                f1.write(str(row)+'\n')
            last_one=div[0].find_all('td')[0].get_text()                   
        # break
    f1.close()
# get_link_two()

def get_link_three():
    f=open('link_two.txt','a+',encoding='utf-8')
    for line in open('link_one.txt','r',encoding='utf-8'):
        line=eval(line)
        print(line[:3])
        root='https://yz.chsi.com.cn'
        url=root+line[3]
        print(url)
        req=requests.get(url,headers=header)
        bsObj=BeautifulSoup(req.text,'html.parser')
        div=bsObj.find('div',class_='zsml-list-box').find('table',class_='ch-table').find('tbody').find_all('tr')
        if len(div)>=10:
            print(url+'超过10个')
        for tr in div:
            row=[]+line
            td_list=tr.find_all('td')
            row.append(td_list[0].get_text())#考试方式
            row.append(td_list[1].get_text())#院系所
            row.append(td_list[2].get_text())#专业
            row.append(td_list[3].get_text())#研究方向
            row.append(td_list[4].get_text())#学习方式
            row.append(td_list[5].get_text())#指导教师
            row.append(td_list[8].get_text())#跨专业
            #拟招生人数
            # print(td_list[9])
            row.append(re.search(r"cutString\('(.+?)'",str(td_list[6])).group(1))
            # row.append(td_list[6].find('a').attrs['data-title'])
            #备注
            try:
                row.append(re.search(r"cutString\('(.+?)'",str(td_list[9])).group(1))
            except:
                row.append('')
            
            # row.append(td_list[9].find('a').attrs['data-title'])
            #考试范围查看
            row.append(td_list[7].find('a').attrs['href'])
            # print(row)
            f.write(str(row)+'\n')
        # break
        # last_one=div[0].find_all('td')[0].get_text()
    f.close()


def final_chakan(line):
    line=eval(line)      
    root='https://yz.chsi.com.cn'
    url=root+line[-1]
    print(url)
    try:
        req=requests.get(url,headers=header,timeout=5)
    except:
        f_error.write(str(line)+'\n')
        return
    bsObj=BeautifulSoup(req.text,'html.parser')
    tbody_list=bsObj.find_all('tbody',class_='zsml-res-items')
    row=line
    for tbody in tbody_list:
        tr_list=tbody.find_all('tr')
        for tr in tr_list:
            text=''
            td_list=tr.find_all('td')
            for td in td_list:
                text=text+'_'+td.get_text().replace('\n','').strip().replace('见招生简章','').replace('\r','')
            row.append(text)  
    f.write(str(row)+'\n')
    print('写入')

# f=open('link_add_chakan2.txt','a+',encoding='utf-8')
# f_error=open('error4.txt','w+',encoding='utf-8')

# executor = ThreadPoolExecutor(max_workers=6)
# task_list = [executor.submit(final_chakan, line) for line in open('link_two.txt','r',encoding='utf-8')]

# for line in open('error2.txt','r',encoding='utf-8'):
#     final_chakan(line)

# f.close()
# f_error.close()

# 写到csv
# f1=open('硕士专业目录.csv','w+',encoding='gb18030',newline='')
# csv_write=csv.writer(f1)
# for line in open('link_add_chakan.txt','r',encoding='utf-8'):
#     line=eval(line)
#     row=[]
#     line[5]=line[5].replace('985\u2002211','985 211').replace('985??211','985 211')    
#     row=line[:3]+line[4:18]
#     for i in range(19,len(line)):
#         m=line[i].replace(' ','').replace('详见我校研究生院主页或研招网招生简章','').split('_')
#         csv_write.writerow(row+m)

# for line in open('link_add_chakan2.txt','r',encoding='utf-8'):
#     line=eval(line)
#     row=[]
#     line[5]=line[5].replace('985\u2002211','985 211').replace('985??211','985 211')    
#     row=line[:3]+line[4:18]
#     for i in range(19,len(line)):
#         m=line[i].replace(' ','').replace('详见我校研究生院主页或研招网招生简章','').split('_')
#         csv_write.writerow(row+m)

x1 = xlrd.open_workbook("硕士专业目录.xlsx")   
table = x1.sheet_by_name(u"硕士专业目录")
nrows = table.nrows
r=0
workbook = xlsxwriter.Workbook('last硕士专业目录.xlsx') #创建工作簿
sheet = workbook.add_worksheet()
for j in range(nrows):
    if j<121957:
        continue
    if r>=60000:
        #新建文件
        print(j)
        workbook.close()
        workbook = xlsxwriter.Workbook(str(j)+'硕士专业目录.xlsx') #创建工作簿
        sheet = workbook.add_worksheet()
        r=0
    line=table.row_values(j)
    # print(len(line))
    # break
    row=[]
    row=line[:17]
    for i in range(17,len(line)):
        # print(line[i])
        if line[17]=='':
            for l in range(len(row)):
                sheet.write(r,l,row[l])
            r=r+1
            break
        if line[i]=='':
            break
        m=line[i].replace(' ','').replace('详见我校研究生院主页或研招网招生简章','').split('_')
        t=row+m
        for l in range(len(t)):
            sheet.write(r,l,t[l])
        r=r+1
workbook.close()
        


