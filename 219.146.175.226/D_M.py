from bs4 import BeautifulSoup
import requests
import time
import datetime
import json
import re
import xlsxwriter




def get_data(code):
    data={
        'Method':'QueryHistoryReport',
        'index':1,
        'sort':0,
        'YWGS':'',
        'showValidate':0,   
        'showUpload':0,
        'page':1,
        'rows':1,
    }
    today=str(datetime.date.today())
    yes=str(datetime.date.today() + datetime.timedelta(days=-1))
    data['start']=yes+' 00:00:00'
    data['end']=today+' 23:59:59'
    if code=='1688' or code=='1696' or code=='14095':
        data['multiCode']='201,203,207,205,210'
        data['codes']='201,203,207,209,525,210,545,546,205,221'
        if code=='1688':            
            data['subid']='1668'
            data['subname']='东明石化1'
        
        if code=='1696':
            data['subid']='1696'
            data['subname']='东明石化2'
        if code=='14095':
            data['subid']='14095'
            data['subname']='东明中油燃料石化有限公司'
    if code=='1671':
        data['subid']='1671'
        data['subname']='东明石化集团'
        data['multiCode']='311,313,316,466,494'
        data['codes']='316,311,494,302'

    return data
def main(sheet,workbook,format3):
    # 2
    url='http://219.146.175.226:8406/webs/ajax/WasteWater/QueryAnalysis/HistoryReportQUIDYN/HistoryReport.ashx'
    for u in range(5):
        try:
            req=requests.post(url,headers=header,data=get_data('1671'))
            js=json.loads(req.text)['rows'][0]
            break
        except:
            pass
        if u==4:
            print('请检查网络连接以及网站是否异常')
            return
            
    # print(js)
    sheet.write('A32',js['DateTime'],workbook.add_format({
        'border':1,
        'font_size':11,  
        'font_color': 'green',
        
    }))
    sheet.write('B32',js['val_316'],format3)
    sheet.write('C32',js['flow_316'],format3)
    sheet.write('D32',js['val_311'],format3)
    sheet.write('E32',js['flow_311'],format3)
    sheet.write('F32',js['flow_494'],format3)
    sheet.write('G32','',format3)
    # 1
    url='http://219.146.175.226:8406/webs/ajax/WasteGas/QueryAnalysis/HistoryReportQUIDYN/HistoryReport.ashx'
    codelist=[1688,1696,14095]
    for i in range(3):
        code=codelist[i]
        rw=1+i*9
        for u in range(5):
            try:
                req=requests.post(url,headers=header,data=get_data(str(code)))
                js=json.loads(req.text)['rows'][0]
                break
            except:
                pass
        if u==4:
            print('请检查网络连接以及网站是否异常')
            return
        # print(js)
        sheet.write('A'+str(rw+4),js['DateTime'],workbook.add_format({
        'border':1,
        'font_size':11,  
        'font_color': 'green',
        
            }))
        sheet.write('A'+str(rw+8),js['DateTime'],workbook.add_format({
        'border':1,
        'font_size':11,  
        'font_color': 'green',

            }))
        sheet.write('B'+str(rw+4),js['val2_201'],format3)
        sheet.write('C'+str(rw+4),js['cvt_201'],format3)
        sheet.write('D'+str(rw+4),js['ex_201'],format3)
        sheet.write('E'+str(rw+4),js['val_203'],format3)
        sheet.write('F'+str(rw+4),js['cvt_203'],format3)
        sheet.write('G'+str(rw+4),js['ex_203'],format3)
        sheet.write('B'+str(rw+8),js['val2_207'],format3)
        sheet.write('C'+str(rw+8),js['cvt_207'],format3)
        sheet.write('D'+str(rw+8),js['ex_207'],format3)
        sheet.write('E'+str(rw+8),js['val2_209'],format3)
        sheet.write('F'+str(rw+8),js['val2_525'],format3)
        sheet.write('G'+str(rw+8),js['val2_210'],format3)
        # sheet.write('G'+str(rw+8),js['val2_210'],format3)
    print(js['DateTime']+'正在写入')


def write_xlsx(cook):
    workbook = xlsxwriter.Workbook('站点实时信息.xlsx')     #创建工作簿
    sheet = workbook.add_worksheet()
    # bold=workbook.add_format({'border':2})
    merge_format1 = workbook.add_format({
    # 'bold':     True,
    'border':   1,
    'align':    'center',#水平居中
    # 'valign':   'vcenter',#垂直居中
    # 'fg_color': 'green',#颜色填充
    'font_color': 'green',
    'font_size':12,  
    })
    merge_format2 = workbook.add_format({
        # 'bold':     True,
        'border':   1,
        'align':    'center',#水平居中
        # 'valign':   'vcenter',#垂直居中
        # 'fg_color': 'green',#颜色填充
        'font_color': 'green',
        
        'font_size':14,  
    })
    format3=workbook.add_format({
        'border':1,
        'font_size':12,  
        # 'fg_color': 'green',#颜色填充
        'font_color': 'green',
        
    })
    sheet.set_column('A:A', 13)   
    sheet.set_column('B:G', 11)   
    
    for i in range(1,26,9):
        rw=i
        sheet.merge_range('A'+str(rw+1)+':A'+str(rw+3),'时间',workbook.add_format({
    # 'bold':     True,
    'border':   1,
    'align':    'center',#水平居中
    # 'valign':   'vcenter',#垂直居中
    # 'fg_color': 'green',#颜色填充
    'font_color': 'green',
    'font_size':14,  
    }))
        sheet.merge_range('A'+str(rw+5)+':A'+str(rw+7),'时间',workbook.add_format({
    # 'bold':     True,
    'border':   1,
    'align':    'center',#水平居中
    # 'valign':   'vcenter',#垂直居中
    # 'fg_color': 'green',#颜色填充
    'font_color': 'green',
    'font_size':14,  
    }))
        sheet.merge_range('B'+str(rw+1)+':D'+str(rw+1),'二氧化硫',merge_format1)
        sheet.merge_range('E'+str(rw+1)+':G'+str(rw+1),'氮氧化物',merge_format1)
        sheet.merge_range('B'+str(rw+5)+':D'+str(rw+5),'颗粒物',merge_format1)
        sheet.write('E'+str(rw+5),'氧含量',format3)
        sheet.write('F'+str(rw+5),'烟气温度',format3)
        sheet.write('G'+str(rw+5),'废气排放量',format3)

        sheet.write('B'+str(rw+2),'实测浓度',format3)
        sheet.write('C'+str(rw+2),'折算浓度',format3)
        sheet.write('D'+str(rw+2),'排放量',format3)
        sheet.write('E'+str(rw+2),'实测浓度',format3)
        sheet.write('F'+str(rw+2),'折算浓度',format3)
        sheet.write('G'+str(rw+2),'排放量',format3)
        sheet.write('B'+str(rw+6),'实测浓度',format3)
        sheet.write('C'+str(rw+6),'折算浓度',format3)
        sheet.write('D'+str(rw+6),'排放量',format3)
        sheet.write('E'+str(rw+6),'（%）',format3)
        sheet.write('F'+str(rw+6),'（C°）',format3)
        sheet.write('G'+str(rw+6),'(m3/h)',format3)
        for j in range(2):
            sheet.write('B'+str(rw+3+j*4),'(mg/M3)',format3)
            sheet.write('C'+str(rw+3+j*4),'(mg/M3)',format3)
            sheet.write('D'+str(rw+3+j*4),'(kg)',format3)
            sheet.write('E'+str(rw+3+j*4),'',format3)
            sheet.write('F'+str(rw+3+j*4),'',format3)
            sheet.write('G'+str(rw+3+j*4),'',format3)
        sheet.write('E'+str(rw+3),'(mg/M3)',format3)
        sheet.write('F'+str(rw+3),'(mg/M3)',format3)
        sheet.write('G'+str(rw+3),'(kg)',format3)
    sheet.merge_range('A29:A31','时间',workbook.add_format({
    # 'bold':     True,
    'border':   1,
    'align':    'center',#水平居中
    # 'valign':   'vcenter',#垂直居中
    # 'fg_color': 'green',#颜色填充
    'font_color': 'green',
    'font_size':14,  
    }))
    sheet.merge_range('B29:C29','化学需氧量',merge_format1 )
    sheet.merge_range('D29:E29','氨氮',merge_format1 )
    sheet.write('F29','小时流量',merge_format1 )
    sheet.merge_range('G29:G31','PH',workbook.add_format({
        'border':   1,
        'align':    'center',#水平居中
        'valign':   'vcenter',#垂直居中
        'font_color': 'green',
        'font_size':12,  
    }))
    sheet.write('B30','浓度',merge_format1 )
    sheet.write('C30','排放量',merge_format1 )
    sheet.write('D30','浓度',merge_format1 )
    sheet.write('E30','排放量',merge_format1 )
    sheet.write('F30','(m³/h)',merge_format1 )
    sheet.write('B31','（mg/l)',merge_format1 )
    sheet.write('C31','(kg)',merge_format1 )
    sheet.write('D31','（mg/l)',merge_format1 )
    sheet.write('E31','(kg)',merge_format1 )

    sheet.merge_range('A1:G1','东明石化1',merge_format2)
    sheet.merge_range('A10:G10','东明石化2',merge_format2)
    sheet.merge_range('A19:G19','东明中油燃料石化有限公司（催化车间）',merge_format2)
    sheet.merge_range('A28:G28','东明石化集团（废水总排口）',merge_format2)
    main(sheet,workbook,workbook.add_format({
        'border':1,
        'font_size':14,  
        'font_color': 'green',
        
    }))
    workbook.close()
# write_xlsx()

# cook='autoLogin=null; user=null; pwd=null; ASP.NET_SessionId=d2xbq3ygtgvllt55bkxj4jvm'
cook=input('请输入Cookie：')
header={
    'Cookie':cook,
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
}
t=900
while True:
    write_xlsx(cook)
    print('写入完毕')
    time.sleep(t)




 
