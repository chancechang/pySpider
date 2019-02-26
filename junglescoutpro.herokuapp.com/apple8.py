

import requests
import csv
import json
import time
import math

MAX_Page=40000
each=200
end=math.ceil(MAX_Page/each)+1

searchText='apple 8'

minPrice=2000
minRank=0
maxRank=100000

def getObj(url):
    for i in range(3):
        try:
            html=requests.get(url,headers=headers)
            return html
        except:
            pass     
    return None  


data={
    'email':'1441839327@qq.com',
    'password':'gsd753951'
}
loginUrl='https://junglescoutpro.herokuapp.com/users/sign_in'
response=requests.post(loginUrl,data)
token=json.loads(response.text)['data']['token']

headers = {
    'Authorization':'Bearer '+token,
    }
urlroot1='https://junglescoutpro.herokuapp.com/api/products/get_products?data%5Bquery%5D%5Btype%5D=query&data%5Bquery%5D%5BsearchTerm%5D='+str(searchText).replace(' ','%20')+'&data%5Bquery%5D%5BqueryFields%5D%5B%5D=name&data%5Bquery%5D%5BqueryFields%5D%5B%5D=brand&data%5Bquery%5D%5BqueryFields%5D%5B%5D=asin&data%5Bcountry%5D%5Btype%5D=terms&data%5Bcountry%5D%5BvaluesArray%5D%5B%5D=us&data%5Bsort%5D%5Btype%5D=sort&data%5Bsort%5D%5Bcolumn%5D=name&data%5Bsort%5D%5Bdirection%5D=asc&data%5Bpaginate%5D%5Btype%5D=paginate&data%5Bpaginate%5D%5BpageSize%5D='+str(each)
urlroot2='&data%5BisComplete%5D%5Btype%5D=terms&data%5BisComplete%5D%5BvaluesArray%5D%5B%5D=true&data%5Bstate%5D%5Btype%5D=terms&data%5Bstate%5D%5BvaluesArray%5D%5B%5D=active&skipCounter=false'
if minPrice!=0:
    urlroot1=urlroot1+'&data%5Bprice%5D%5Btype%5D=range&data%5Bprice%5D%5Bmin%5D='+str(minPrice)
if minRank!=0 or maxRank!=100000:
    urlroot1=urlroot1+'&data%5Brank%5D%5Btype%5D=range'
    if minRank!=0:
        urlroot1=urlroot1+'&data%5Brank%5D%5Bmin%5D='+str(minRank)
    if maxRank!=100000:
        urlroot1=urlroot1+'&data%5Brank%5D%5Bmax%5D='+str(maxRank)


date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
f1=open(date+'jungle_'+searchText.replace(' ','_')+'.csv','w+',encoding='gb18030',newline='')
csv_write=csv.writer(f1)
colname=['asin','name','brand','sellerName','rawCategory','price','fees','net','weight','tier','nReviews','rating','rank','estimatedSales','estRevenue','listingQualityScore','nSellers','imageUrl']
csv_write.writerow(colname)
t=0
for i in range(0,end):
    url=urlroot1+'&data%5Bpaginate%5D%5Bfrom%5D='+str(t)+urlroot2
    bsObj=getObj(url)
    try:
        products=json.loads(bsObj.text)['data']['data']['products']
    except:
        print('爬取了'+str(t+1)+'条数据,结束')
        break
    print('爬取了'+str(t)+'条数据')
    t=t+len(products)
    if len(products)==0:
        print('爬取了'+str(t+1)+'条数据,结束')  
        break      
    for p in products:
        row=['N.A.' for i in range (0,18)]
        for i in range(0,18):
            c=colname[i]
            if c in p:
                row[i]=p[c]
        csv_write.writerow(row)
    time.sleep(2)
