from bs4 import BeautifulSoup
import requests
import xlsxwriter
import  numpy as np
import xlrd
from  decimal import Decimal

def get_data():
    f=open('aepb.txt','a+',encoding='utf-8',newline='')
    for i in range(1,1963):
        # url='http://www.aepb.gov.cn/pages/SJZX_List.aspx?CityCode=340800&LX=6&KSSJ=2018-01-01%2008&JSSJ=2018-12-31%2008
        url='http://www.aepb.gov.cn/pages/SJZX_List.aspx?CityCode=340800&LX=6&KSSJ=2018-01-01%2000&JSSJ=2018-12-13%2023&page='+str(i)
        req=requests.get(url)
        bsObj=BeautifulSoup(req.text,'html.parser')
        # print(bsObj)
        trlist=bsObj.find('table',class_='data_table').find_all('tr')
        for j in range(1,len(trlist)):
            tr=trlist[j]
            tdlist=tr.find_all('td')
            row=[]
            for td in tdlist:
                row.append(td.get_text().replace('\n','').replace('\r','').strip())
            f.write(str(row)+'\n')
    f.close()




def write_xlsx():
    workbook = xlsxwriter.Workbook('2018aepb.xlsx')     #创建工作簿
    sheet = workbook.add_worksheet()
    r=0
    # for i in range(len(rowname)):
    #         sheet.write(r,i,rowname[i])
    # r=1
    for line in open('aepb.txt','r',encoding='utf-8'):
        line=eval(line)
        for i in range(len(line)):
            sheet.write(r,i,line[i])
        r=r+1
    workbook.close()
# write_xlsx()


def get_mean():
    workbook = xlsxwriter.Workbook('2017aepb_max_min.xlsx')     #创建工作簿
    sheet = workbook.add_worksheet()
    rw=0

    xl = xlrd.open_workbook("2017aepb_mean.xlsx")
    sheet1 = xl.sheet_by_name("Sheet1")
    now_title='怀宁县青妇活动中心'
    now_time=''
    # print(sheet1.ncols)
    w_row=['-' for i in range(2)]
    data_list=[[] for i in range(7)]
    for r in range(sheet1.nrows):
        row=sheet1.row_values(r) 
        if row[1][:2]!=now_time or r==sheet1.nrows-1:
            if now_time!='' : 
                #时间变了，就写入，
                #写入
                w_row[0]=now_title
                w_row[1]=now_time[:2]
                print(str(w_row[:2])+'xireu')
                # w_row=w_row+[str(Decimal(np.mean(data_list[j])).quantize(Decimal('0.000'))) if data_list[j]!=[] else '--'  for j in range(7)]
                
                w_row=w_row+[str(Decimal(np.min(data_list[j])).quantize(Decimal('0.000')))+'~'+str(Decimal(np.max(data_list[j])).quantize(Decimal('0.000'))) if data_list[j]!=[] else '--'  for j in range(7)]
                for i in range(len(w_row)):
                    sheet.write(rw,i,w_row[i])
                # print(w_row)
                rw=rw+1
                #清空一波
                data_list=[[] for i in range(7)]
                w_row=['' for i in range(2)]
                #检查一下名字变了没
                if row[0]!=now_title:
                    now_title=row[0]
            now_time=row[1][:2]
            
        #读取数据
        for d in range(7):
            try:
                #计算均值
                # data_list[d].append(float(row[d+1]))
                #计算最大最小
                data_list[d].append(float(row[d+2]))
               
            except:
                # print(row[d+1])
                pass
            #存储数据
    workbook.close()
get_mean()    


