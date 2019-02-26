
import requests
import csv
import json
import sys
sys.path.append('..')
import mytemp
import re
import time
import xlsxwriter
import pandas as pd

person ={}
p_name ={}
person_ids =[]


def getData(id,ty):
    data={
        'autoguid':id,
        'infotype':ty
    }
    return data
def req_post(url,data):
    for i in range(5):
        try:
            req=requests.post(url, data, timeout=10)
            return (req.text)
        except:
            time.sleep(10)
        if i==4:
            print(url)
          

#key为人，value为list,0为配偶，1为父亲，2为母亲，3为兄弟,4为姐妹，5为儿子，6为女儿  
def get_json(id,son_peou,ty):
    global person
    global p_name
    global person_ids
    print('get_json', son_peou ,id)
    if son_peou=='son':
        # print(id+'  son')
        data=getData(id,ty)
        tx=req_post('http://zupu.syshenshi.com/ashx/ZTree.ashx',data)
        js=json.loads(tx)
        if len(js)==0:
            return
        for d in js:
            son_id=d['autoguid']
            name=d['tree_infoname']
            #建立自己的基本信息
            p_name[son_id]=name
            person[son_id]=['' for i in  range(7)]
            person_ids.append(son_id)
            #为儿子写上父母
            person[son_id][1]=id
            person[son_id][2]=person[id][0]            
            #补充父亲的儿子信息            
            if '女' in name:
                person[id][6]=person[id][6]+son_id+' '
                get_json(son_id,'peou',ty)
            else: 
                person[id][5]=person[id][5]+son_id+' '
                get_json(son_id,'peou',ty)
                get_json(son_id,'son',ty)
        #for 循环结束再写兄弟姐妹 
        per_son=person[id][5].split(' ')[:-1]
        per_dau=person[id][6].split(' ')[:-1]
        for s in per_son:
            for j in per_son:
                if s!=j:
                    person[s][3]=person[s][3]+j+' '
            for j in per_dau:
                person[s][4]=person[s][4]+j+' '
        for s in per_dau:
            for j in per_dau:
                if s!=j:
                    person[s][4]=person[s][4]+j+' '
            for j in per_son:
                person[s][3]=person[s][3]+j+' '
    else:       
        peouUrl='http://zupu.syshenshi.com/ashx/Zuren.ashx?act=getpeou&autoguid='+id
        tx=req_post(peouUrl,{})
        js=json.loads(tx)
        if len(js)==0:
            return
        # peou不需要person,只需要单独信息页面
        for d in js:
            peou_id=d['autoguid']
            name=d['infoname']
            # 为自己加上信息
            p_name[peou_id]=name
            #为丈夫加上自己信息
            person[id][0]=person[id][0]+peou_id+' '

def main3(ty):
    #个人信息页写入
    f_detail=open('P_detail'+str(ty)+'.txt','w+',newline='',encoding='utf-8')
    # f3=open('82.txt','w+',enc)
    for line in open('p_name'+str(ty)+'.txt','r',encoding='utf-8'):
        line=eval(line)
        if line[0]=='0':
            continue
        url='http://zupu.syshenshi.com/zuren_detail.aspx?id='+line[0]
        print(url)
        try:
            bsObj=mytemp.getObj(url)
            trlist=bsObj.find('table',class_='stdtable').find('tbody').find_all('tr')
        except:
            time.sleep(20)
            try:
                bsObj=mytemp.getObj(url)
                trlist=bsObj.find('table',class_='stdtable').find('tbody').find_all('tr')
            except:
                time.sleep(20)
                bsObj=mytemp.getObj(url)
                trlist=bsObj.find('table',class_='stdtable').find('tbody').find_all('tr')
        row=line+[]
        for tr in trlist:
            tdlist3=tr.find_all('td',class_='center')
            for td in tdlist3:
                row.append(td.get_text().replace(" ",''))
            tdlist=tr.find_all('td',class_='left')
            for td in tdlist:
                row.append(td.get_text().replace(" ",''))
        if len(row)==31 and len(line)!=33:                
            row=row[:26]+['','']+row[26:]
        f_detail.write(str(row)+'\n')
    f_detail.close()
        

def main2():
    j=0
    global person
    global p_name
    global person_ids    
    for line in open('zupu1.txt','r',encoding='utf-8'):
        person = {}
        p_name = {}
        person_ids = []
        line=eval(line)
        print(line)
        ty=re.search(r'&infotype=(.+?)$',line[1]).group(1)
        print(ty)
        f2=open('zupushuid'+str(ty)+'.txt','w+',encoding='utf-8')
        p_name['0']='根'
        person['0']=['' for i in range(7)]    
        get_json('0','son',ty)
        for id in person_ids:   
            f2.write(str([id]+person[id])+'\n')
        f2.close()
        f3=open('p_name'+str(ty)+'.txt','w+',encoding='utf-8')
        for key, value in p_name.items():
            f3.write(str([key,value])+'\n')
        f3.close()
        j=j+1 
        main3(ty)     
main2()   


def main1():
    #族谱总链接
    f1=open('zupu.txt','w+',encoding='utf-8')
    for i in range(1,100):
        url='http://zupu.syshenshi.com/Index.aspx?pageindex='+str(i)+'&infoname='
        bsObj=mytemp.getObj(url)
        trlist=bsObj.find('table',class_='stdtable').find('tbody').find_all('tr')
        le=len(trlist)
        print(le)
        if le==0:
            break
        for tr in trlist:
            td=tr.find('td')
            name=td.get_text()
            href=td.find('a').attrs['href']
            row=[name,href]
            print(row)
            f1.write(str(row)+'\n')

def main5():
    '获取个人信息页'
    f5=open('personal_info.csv','w+',newline='',encoding='gb18030')
    csv_write5=csv.writer(f5)
    f6=open('personal_info.txt','w+',encoding='utf-8')
    for i in range(0,52672):
        url='http://zupu.syshenshi.com/ZR.aspx?pageindex='+str(i)+'&infoname=&mobile=&infotype=&infotype_name=&industry=&address=&iswaiqian=0&fuqin=&muqin=&peiou=&zinv=&muyuandizhi=&waiqiandizhi=&chushengriqi_begin=&chushengriqi_end=&qushiriqi_begin=&qushiriqi_end=&waiqian_begin=&waiqian_end='
        bsObj=mytemp.getObj(url)
        trlist=bsObj.find('table',class_='stdtable').find('tbody').find_all('tr')
        for tr in trlist:
            tdlist=tr.find_all('td')
            row=[]
            for td in tdlist:
                if td.find('a')!=None:
                    row.append(td.find('a').attrs['href'])
                row.append(td.get_text())
            f6.write(str(row)+'\n')
            csv_write5.writerow(row)
        break
 
