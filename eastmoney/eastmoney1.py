from bs4 import BeautifulSoup
import requests
import csv
import sys
import json
import datetime
sys.path.append("..")

def writetoCsv(filename,writelist,header=None):
    out=open(filename, 'w+',encoding='gb18030',newline = '')
    csv_write=csv.writer(out)
    if header!=None:
        csv_write.writerow(header)
    for wlist in writelist:
        csv_write.writerow(wlist)
url='http://ff.eastmoney.com/EM_CapitalFlowInterface/api/js?id=ls&type=ff&check=MLBMS&cb=var%20aff_data=&js={(x)}&rtntype=3&acces_token=1942f5da9b46b069953c873404aad4b5&_=1533126996896'
r=requests.get(url)
data=json.loads(r.text.replace('var aff_data=',''))
data['xa']=data['xa'].split(',')
# print(data['ya'][0])
target=[]
for i in range(len(data['xa'])-1):
    data['ya'][i]=data['ya'][i].split(',')
    target.append([data['xa'][i]]+data['ya'][i])
# ['时间','主力净流入','超大单净流入','','','']
nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

writetoCsv('实时资金流向'+nowTime[:10]+'.csv',target)

