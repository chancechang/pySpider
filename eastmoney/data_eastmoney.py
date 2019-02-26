from bs4 import BeautifulSoup
import requests
import re
import json
import datetime
import time
import xlsxwriter

def get_json(url):
    for i in range(5):
        try:
            req=requests.get(url,timeout=15)
            data=re.search(r'data:(.+?),dataUrl',req.text).group(1)
            js=json.loads(data)
            le=len(js)
            # print(le)
            # if le<50:
            #     print(str(le)+'  '+i)
            return js
        except:
            time.sleep(2)
            pass
    return None
def main():
    year=2015
    f=open(str(year)+'eastmoney.txt','w+',encoding='utf-8')
    # url='http://data.eastmoney.com/zlsj/zlsj_list.aspx?type=ajax&st=1&sr=-1&p=2&ps=50&jsObj=sExHEeNF&stat=1&cmd=1&date=2017-12-31&rt=51444268'
    i=1

    while True:
        print(i)
        time.sleep(2)
        url='http://data.eastmoney.com/zlsj/zlsj_list.aspx?type=ajax&st=1&sr=-1&p='+str(i)+'&ps=50&jsObj=ZFQdbwxX&stat=1&cmd=1&date='+str(year)+'-12-31'
        js=get_json(url)

        for j in js:
            row=[year,j['SCode'],j['SName'],j['Count']]
            # print(row)
            f.write(str(row)+'\n')
        i=i+1
        if len(js)<50:
            break
        # break
    f.close()
main()
year=2017
workbook=xlsxwriter.Workbook('eastmoney2012-17.xlsx')
sheet=workbook.add_worksheet()
r=0
while year>=2012:
    for line in open(str(year)+'eastmoney.txt','r+',encoding='utf-8'):
        line=eval(line)
        for i in range(4):
            sheet.write(r,i,line[i])
        r=r+1
    
    year=year-1
workbook.close()