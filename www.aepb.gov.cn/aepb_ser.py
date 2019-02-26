
from bs4 import BeautifulSoup
import requests
import time

def get_data():
    f=open('aepb.txt','a+',encoding='utf-8',newline='')
    error=[]
    for i in range(1,1963):
        print(i)
        # url='http://www.aepb.gov.cn/pages/SJZX_List.aspx?CityCode=340800&LX=6&KSSJ=2018-01-01%2008&JSSJ=2018-12-31%2008&page='+str(i)
        url='http://www.aepb.gov.cn/pages/SJZX_List.aspx?CityCode=340800&LX=6&KSSJ=2018-01-01%2000&JSSJ=2018-12-13%2023&page='+str(i)
        for m in range(5):
            try:
                req=requests.get(url)
                bsObj=BeautifulSoup(req.text,'html.parser')
                # print(bsObj)
                trlist=bsObj.find('table',class_='data_table').find_all('tr')
                break
            except:
                time.sleep(3)
            if m==4:
                print('第'+str(i)+'页爬取失败')
                error.append(i)
                trlist=None
        if trlist==None:
            continue

        for j in range(1,len(trlist)):
            tr=trlist[j]
            tdlist=tr.find_all('td')
            row=[]
            for td in tdlist:
                row.append(td.get_text().replace('\n','').replace('\r','').strip())
            f.write(str(row)+'\n')
    print(error)
    f.close()
get_data()