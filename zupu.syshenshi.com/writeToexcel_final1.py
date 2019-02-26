
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

def main7(id,ty):
    line=[]
    for line in open('./zupu1/p_name'+str(ty)+'.txt','r',encoding='utf-8'):
        line=eval(line)
        if line[0]==id:
            print('right')
            break
    if line[0]!=id:
        return 'no'
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

def main6(ty):
    f1=open('./zupu1/P_detail_final'+str(ty)+'.csv','w+',newline='',encoding='gb18030')
    csv_write1=csv.writer(f1)
    try:
        
        for line in open('./zupu1/P_detail'+str(ty)+'.txt','r',encoding='utf-8'):
            line=eval(line)
            if  '否' in  line[25]:
                if len(line)==31:
                    line=line[:26]+['','']+line[26:]                    
                # print(line[25].strip(),len(line))
            csv_write1.writerow(line)
    except:
        for line in csv.reader(open('./zupu1/P_detail'+str(ty)+'.csv','r',encoding='gb18030')):
            if  '否' in  line[25]:
                if len(line)==31:
                    line=line[:26]+['','']+line[26:]                    
                # print(line[25].strip(),len(line))
            csv_write1.writerow(line)
    f1.close()

def main4(ty,filename,workbook):
    LEN=[1,10,1,10,12,12,12,12]
     #创建一个文件
    worksheet_1 = workbook.add_worksheet(filename) 
    colMax=0
    rown=['自己','配偶','父亲','母亲','兄弟','姐妹','儿子','女儿']
    rowname=[]
    for i in range(8):
        colMax=colMax+LEN[i]
        rowname=rowname+[rown[i] for j in range(LEN[i])]  
    # print(colMax)
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
    # print(rowname)
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

    main6(ty)
    try:
        df1 = pd.DataFrame(pd.read_csv('./zupu1/P_detail_final'+str(ty)+'.csv',header=None,encoding='gb18030',))
    except:
        main6(ty)
        try:
            df1 = pd.DataFrame(pd.read_csv('./zupu1/P_detail_final'+str(ty)+'.csv',header=None,encoding='gb18030',))
        except:
            return
        
    df1.fillna('N\A',inplace=True)
    r=2
    for id_format  in open('./zupu1/zupushuid'+str(ty)+'.txt','r'):
        col=-1
        id_format=eval(id_format)
        if id_format[0]=='0':
            continue
        #写上序号和世代
        mainid=id_format[0]
        row=df1.loc[df1[0]==mainid].values
        if len(row)==0:
            print(mainid)
            row=main7(mainid,ty)
            if row=='no':
                continue
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
                    id_list=id_list[:LEN[j]]
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
                    row=main7(id,ty)
                    if row=='no':
                        continue
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

def main8():
    #写入excel
    j=0
    page=17
    print('page'+str(page))
    num=10
    page_max=18
    zupufile='zupu_full'
    workbook = xlsxwriter.Workbook('excel_page'+str(page)+'_final.xlsx')
    for line in open(zupufile+'.txt','r',encoding='utf-8'):
        line=eval(line)
        ty=re.search(r'&infotype=(.+?)$',line[1]).group(1)
        # ty='85'
        print(ty)    
        zupuname=re.search(r'jiapuName=(.+?)&infotype=',line[1]).group(1)
        if len(zupuname)>=30:
            zupuname=zupuname[:10]+'...'+zupuname[-10:]
        main4(ty,zupuname,workbook)
        j=j+1 
        if j==num:
            j=0
            workbook.close()
            page=page+1
            print('page'+str(page))
            workbook = xlsxwriter.Workbook('excel_page'+str(page)+'_final.xlsx')
        if page==page_max:
            break
            # break  
    workbook.close()
main8()