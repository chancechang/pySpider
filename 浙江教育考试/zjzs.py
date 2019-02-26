# http://zt.zjzs.net/xuanke2018/allcollege.html

from bs4 import BeautifulSoup
import requests
import csv

root='http://zt.zjzs.net/xuanke2018/'

c=requests.get(root+'allcollege.html',timeout=10) 
c.encoding = 'utf-8'
soup=BeautifulSoup(c.text,'html.parser')
trlist= soup.find_all('tr')
out=open('zjzs.csv', 'w+',encoding='gb18030',newline = '')
csv_write=csv.writer(out)
csv_write.writerow(['学校名称','层次','专业（类）名称','选考科目数','选考科目范围','类中所含专业'])
for i in range(2,len(trlist)):
    tdlist=trlist[i].find_all('td')
    if len(tdlist)<3:
        continue
    print(tdlist[2].string)
    schoolname=tdlist[2].string
    href=tdlist[4].a['href']
    t=requests.get(root+href,timeout=10) 
    t.encoding='utf-8'
    sou=BeautifulSoup(t.text,'html.parser')   
    trlst=sou.find_all('tr')
    for j in range(2,len(trlst),2):
        tdlst=trlst[j].find_all('td')
        if len(tdlst)<3:
            continue
        print([tdlist[2].string,tdlst[0].string,tdlst[1].string,tdlst[2].string,tdlst[3].string,tdlst[4].string])
        csv_write.writerow([tdlist[2].string,tdlst[0].string,tdlst[1].string,tdlst[2].string,tdlst[3].string,tdlst[4].string])
    
