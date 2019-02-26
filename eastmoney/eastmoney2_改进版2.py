import requests
import time
import datetime
import json
import csv

# def get(t):
#     res_text=requests.get('http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=0000011,3990012&sty=CTBFTA&st=z&sr=&p=&ps=&cb=&token=70f12f2f4f091e459a279469fe49eca5').text
#     data=eval(res_text)
#     dh=data[0].split(',')
#     ds=data[1].split(',')
#     # 超大单流入
#     data_1='%.4f'%((float(dh[7]) + float(ds[7])) / 100000000)
#     data_2='%.4f'%((float(dh[8]) + float(ds[8])) / 100000000)
#     data_3='%.4f'%((float(dh[11]) + float(ds[11])) / 100000000)
#     data_4='%.4f'%((float(dh[12]) + float(ds[12])) / 100000000)
#     data_5='%.4f'%((float(dh[15]) + float(ds[15])) / 100000000)
#     data_6='%.4f'%((float(dh[16]) + float(ds[16])) / 100000000)
#     data_7='%.4f'%((float(dh[19]) + float(ds[19])) / 100000000)
#     data_8='%.4f'%((float(dh[20]) + float(ds[20])) / 100000000)
#     datalist=[str(t)[11:16],data_1,data_2,data_3,data_4,data_5,data_6,data_7,data_8]
#     print(datalist)
#     targetData.append(datalist)



# targetData=[]
# while True:
#     nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     if int(str(nowTime)[11:13])>=15 and int(str(nowTime)[14:16])>0:
#         writetoCsv('实时成交'+nowTime[:10]+'.csv',targetData)
#         break
#     elif int(str(nowTime)[11:13])==11 and int(str(nowTime)[14:16])==30:
#         writetoCsv('实时成交'+nowTime[:10]+'.csv',targetData)
#         targetData=[]
#         time.sleep(5340.125)
#     else:
#         try:
#             get(nowTime)    
#         except e:
#             writetoCsv('实时成交'+nowTime[:10]+'.csv',targetData)
#             targetData=[]
#             print('error,attempingting,please wait')
#             get(nowTime)
#     time.sleep(59.875)



import time
from threading  import Timer
#需要补齐包

def getdata():
    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    w.start()
    data0= #需要补齐的内容
    target=[]
    target.append(str(nowTime)[11:19])
    for d in data0.Data :
        target.append(d[0])
    print(target)
    writetoCsv('实时成交'+str(nowTime)[:10]+'.csv',target)
    t=Timer(60,getdata()).start()

def writetoCsv(filename,writelist,header=None):
    out=open(filename, 'a+',encoding='gb18030',newline = '')
    csv_write=csv.writer(out)
    csv_write.writerow(wlist)


t=Timer(60,getdata()).start()
while True:
    if int(str(nowTime)[11:13])>=15 and int(str(nowTime)[14:16])>2:
        t.cancel()
        break
    time.sleep(120)

