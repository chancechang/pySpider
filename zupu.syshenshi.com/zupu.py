
import requests
import csv
import json
import sys
sys.path.append("..")
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
            req=requests.post(url,data,timeout=10)
            return (req.text)
        except:
            time.sleep(10)
        if i==4:
            # print('error')
            print(url)
          

#key为人，value为list,0为配偶，1为父亲，2为母亲，3为兄弟,4为姐妹，5为儿子，6为女儿  
def get_json(id,son_peou,ty,person,p_name):
    
    global person
    global p_name
    global person_ids
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
                get_json(son_id,'peou',ty,person,p_name)
            else: 
                person[id][5]=person[id][5]+son_id+' '
                get_json(son_id,'peou',ty,person,p_name)
                get_json(son_id,'son',ty,person,p_name)
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
def main7(id,ty,page):
    line=[]
    for line in open('./page'+str(page)+'/p_name'+str(ty)+'.txt','r',encoding='utf-8'):
        line=eval(line)
        if line[0]==id:
            print('right')
            break
    if line[0]!=id:
        raise id
    print(line[0])
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
    if len(row)==31:
        row=row[:26]+['','']+row[26:]
    print(row)
    return row
def main3(ty):
    #个人信息页写入
    f_detail=open('P_detail'+str(ty)+'.txt','w+',newline='',encoding='utf-8')
    # f3=open('82.txt','w+',enc)
    for line in open('p_name'+str(ty)+'.txt','r',encoding='utf-8'):
        line=eval(line)
        # print(line)
        if line[0]=='0':
            continue
        # break
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
        row1=[]
        for tr in trlist:
            tdlist3=tr.find_all('td',class_='center')
            for td in tdlist3:
                row.append(td.get_text().replace(" ",''))
            tdlist=tr.find_all('td',class_='left')
            for td in tdlist:
                row.append(td.get_text().replace(" ",''))
        if len(row)==31:
            row=row[:26]+['','']+row[26:]
        f_detail.write(str(row)+'\n')
    f_detail.close()

def main6(ty,page):
    csv_write1=csv.writer(open('./page'+str(page)+'/P_detail'+str(ty)+'.csv','w+',newline='',encoding='gb18030'))
    found=True
    for line in csv.reader(open('./page'+str(page)+'/P_detail'+str(ty)+'.csv','r',encoding='gb18030')):
        # if '68c5a01a-1111-4e34-a9ba-fd1fedf2ca7d'  in line[0]:
        #     found=True
        #     print('found')
        # print(line)
        # break
        if found==True:
            if  '否' in  line[25]:
                if len(line)!=31 and len(line)!=33:
                    print(len(line))
                else:
                    line=line[:26]+['','']+line[26:]
                # print(line[25].strip(),len(line))
            csv_write1.writerow(line)
        # break       
def main4(ty,filename,workbook,page):
    LEN=[0 for i in range(8)]
    for line in open('./page'+str(page)+'/zupushuid'+str(ty)+'.txt','r',encoding='utf-8'):
        line=eval(line)
        if line[0]=='0':
            continue
        for i in range(len(line)):
            ll=line[i].split(' ')
            m=len(ll)
            for l in ll:
                if l=='':
                    m=m-1
            if m>LEN[i]:
                LEN[i]=m
     #创建一个文件
    worksheet_1 = workbook.add_worksheet(filename) 
    colMax=0
    rown=['自己','配偶','父亲','母亲','兄弟','姐妹','儿子','女儿']
    rowname=[]
    for i in range(8):
        colMax=colMax+LEN[i]
        rowname=rowname+[rown[i] for j in range(LEN[i])]  
    print(colMax)
    for line in csv.reader(open('82.csv','r')):
        personalrowname=line
        break
    n=0
    for m in range(len(rowname)):
        if m==0 or '父亲' in rowname[m]:
            continue
        if rowname[m][:2]!=rowname[m-1][:2]:
            n=1
            rowname[m]=rowname[m]+'1'
            n=n+1
            continue
        if rowname[m][:2]==rowname[m-1][:2]:
            rowname[m]=rowname[m]+str(n)
            n=n+1
            continue
    print(rowname)
    personalrowname=['个人信息链接','族谱树姓名']+personalrowname
    # print(personalrowname)
    yellow=workbook.add_format({'border':1,'align':'center','font_size':20})
    # 序号和世都写上
    worksheet_1.write('A1','族谱树链接',)
    tree_link='http://zupu.syshenshi.com/ZPTree.aspx?infotype'+str(ty)
    worksheet_1.write('B1',tree_link,)
    worksheet_1.write('A2','序号',)
    worksheet_1.write('B2','世',)
    for j in range(0,colMax):
        # print(j)
        worksheet_1.merge_range(0,j*33+2,0,j*33+34,rowname[j],yellow)
        for i in range(33):
            worksheet_1.write(1,j*33+2+i,personalrowname[i].replace('：',''))
            # worksheet_1.set_column(j*33+2+i,j*33+2+i+1,30)
    df1 = pd.DataFrame(pd.read_csv('./page'+str(page)+'/P_detail'+str(ty)+'.csv',header=None,encoding='gb18030',))
    df1.fillna('N\A',inplace=True)
    # print(df1.head())
    r=2
    for id_format  in open('./page'+str(page)+'/zupushuid'+str(ty)+'.txt','r'):
        col=-1
        id_format=eval(id_format)
        if id_format[0]=='0':
            continue
        #写上序号和世代
        mainid=id_format[0]
        row=df1.loc[df1[0]==mainid].values
        if len(row)==0:
            print(mainid)
            row=main7(mainid,ty,page)
            try:
                shidai=re.search(r'\[第(.+?)世\]',row[1]).group(1)
            except:
                raise EOFError
        else:
            shidai=re.search(r'\[第(.+?)世\]',row[0][1]).group(1)      
        worksheet_1.write(r,0,str(r-1))
        worksheet_1.write(r,1,shidai)
        for j in range(0,8):
            id_str=id_format[j]
            id_list=id_str.split(' ')
            if len(id_list)<LEN[j]:
                id_list=id_list+['' for t in range(LEN[j]-len(id_list))]
            if len(id_list)>LEN[j]:
                if id_list[-1]=='':
                    id_list=id_list[:-1]
            if len(id_list)!=LEN[j]:
                print('error')
                return
            for id in id_list:
                col=col+1
                if id=='' or id=='0':
                    continue
                row=df1.loc[df1[0]==id].values
                if len(row)==0:
                    print(id)
                    row=main7(id,ty,page)
                    for i in range(32):
                        if i==0:
                            row[i]='http://zupu.syshenshi.com/zuren_detail.aspx?id='+row[0][i]
                        worksheet_1.write(r,col*33+2+i,str(row[i]).strip())
                else:
                    for i in range(32):
                        if i==0:
                            row[0][i]='http://zupu.syshenshi.com/zuren_detail.aspx?id='+row[0][i]
                        worksheet_1.write(r,col*33+2+i,str(row[0][i]).strip())
        r=r+1    

def main2():
    global person
    global p_name
    global person_ids

    j=0
    # 得到族谱树结构
    page=2
    num=1
    for line in open('zupu1.txt','r',encoding='utf-8'):

        person = {}
        p_name = {}
        person_ids = []

        line=eval(line)
        ty=re.search(r'&infotype=(.+?)$',line[1]).group(1)
        # ty='85'
        print(ty)         
        f2=open('zupushuid'+str(ty)+'.txt','w+',encoding='utf-8')
        p_name['0']='根'
        person['0']=['' for i in range(7)]    
        get_json('0','son',ty,person,p_name)
        for key,value in person.items():   
            B_row=[]     
            for i in value:
                if i!='':
                    row=[]
                    i=i.split(' ')[:-1]
                    for t in i:
                        row.append(p_name[t])
                    B_row.append(row)
            f2.write(str([key]+value)+'\n')
        f2.close()
        f3=open('p_name'+str(ty)+'.txt','w+',encoding='utf-8')
        for key, value in p_name.items():
            f3.write(str([key,value])+'\n')
        f3.close()
        j=j+1 
        main3(ty)
        if j==num:
            break  
main2()
def main8():
    #写入excel
    j=0
    page=1
    num=30
    workbook = xlsxwriter.Workbook('excel_page'+str(page)+'_final.xlsx')
    for line in open('zupu1.txt','r',encoding='utf-8'):
        line=eval(line)
        ty=re.search(r'&infotype=(.+?)$',line[1]).group(1)
        # ty='85'
        print(ty)    
        filename=re.search(r'jiapuName=(.+?)&infotype=',line[1]).group(1)
        main4(ty,filename,workbook,page)
        j=j+1 
        if j==num:
            workbook.close()
            break  
# main8()

    



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
