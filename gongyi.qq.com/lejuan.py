from decimal import Decimal
from bs4 import BeautifulSoup
import requests
import time
import datetime
import json
import re
import xlsxwriter

# url='https://gongyi.qq.com/succor/project_list.htm#s_status=3&s_tid=71&p=1'
def get_link():
    f=open('lejuan_first.txt','w+',newline='',encoding='utf-8')
    for i in range(1,678):
        print(i)
        url='https://ssl.gongyi.qq.com/cgi-bin/WXSearchCGI?ptype=stat&s_status=3&s_tid=71&p='+str(i)
        req=requests.get(url)
        text=req.text.replace('(','')[:-1]
        js=json.loads(text)['plist']
        for p in js:
            f.write(str(p)+'\n')
    f.close()
def main():
    f=open('lejuan_detail.txt','a+',newline='',encoding='utf-8')
    f1=open('lejuan_error2.txt','w+',newline='',encoding='utf-8')
    for line in open('lejuan_error1.txt','r',encoding='utf-8'):
        line=line.replace('\n','')
        # line=json.dumps(line)
        # js=json.loads(line)
        # js=json.loads(js)
        print(line)
        # break
        try:
            id=re.search(r'id\': \'(.+?)\',',line).group(1)
        except:
            pass
        print(id)
       
        # obtainMoney=js['donate']['obtainMoney']
        url='https://ssl.gongyi.qq.com/json_data/data_detail/'+str(id)[-2:]+'/detail.'+str(id)+'.js'
        req=requests.get(url)
        text=req.text.replace('_cb_fn_proj_'+str(id)+'(','').replace(');','')
        try:
            data=json.loads(text)
            f.write(json.dumps(data)+'\n')
        except:
            f1.write(line+'\n')
            print(str(id)+'error')
        # print(data)
        # break
    f.close()
    f1.close()

# main()


def analyze():
    workbook = xlsxwriter.Workbook('乐捐_疾病数据.xlsx')     #创建工作簿
    sheet = workbook.add_worksheet()
    lastid=0
    r=0
    rowname=['链接','项目名称','项目开始时间','项目结束时间','项目持续时间（天）','目标金额','已筹金额','完成率','捐赠人数','基金会名称','动态数量','动态频率','捐赠说明字数','捐赠说明图片数目']
    for i in range(len(rowname)):
        sheet.write(r,i,rowname[i])
    r=1
    for line in open('lejuan_detail.txt','r',newline='',encoding='utf-8'):
        # print(line)
        data=json.loads(line)
        base=data['base']
        detail=data['detail']
        try:
            needMoney=float(base['needMoney'])/100.0
        except:
            needMoney=float(base['donate']['needMoney'])/100.0
        #已经获得的钱数
        try:
            obtainMoney=float(base['donate']['obtainMoney'])
            quota_money=float(base['donate']['quota_money'])
            obtainMoney=obtainMoney-quota_money
        except:
            try:
                obtainMoney=float(base['donate']['obtainMoney'])
            except:
                continue
        # 完成率
        try:
            finish=str(Decimal(obtainMoney/needMoney).quantize(Decimal('0.00')))
        except:
            continue
            # finish=1.0
        id=base['id']
        if id == lastid:
            continue
        lastid=id
        title=base['title']
        startTime=base['startTime']
        endTime=base['endTime']
        date1=time.strptime(startTime,"%Y-%m-%d")  
        date2=time.strptime(endTime,"%Y-%m-%d")
        # 项目持续时间
        date1=datetime.datetime(date1[0],date1[1],date1[2])  
        date2=datetime.datetime(date2[0],date2[1],date2[2])  
        #返回两个变量相差的值，就是相差天数  
        try:
            conTime = int(str(date2-date1).split(' ')[0])
        except:
            conTime=1
        
        donateNum=base['donate']['donateNum']
        fundName=base['fundName']

        #进展次数
        try:
            processTime=float(detail['process_total'])
        except:
            processTime=len(detail['process'])
        #频率：
        p=str(Decimal(processTime/int(conTime)).quantize(Decimal('0.00')))
        # p=0
        #捐助说明中字数和频率
        bsObj=BeautifulSoup(detail['desc'],'html.parser')
        imgNum=len(bsObj.find_all('img'))
        count=len(bsObj.get_text())
        row=['https://gongyi.qq.com/succor/detail.htm?id='+str(id),title,startTime,endTime,conTime,needMoney,obtainMoney,finish,donateNum,fundName,processTime,p,count,imgNum]    
        print(row)
        for i in range(len(row)):
            sheet.write(r,i,row[i])
        # break    
        r=r+1
    workbook.close()

analyze()