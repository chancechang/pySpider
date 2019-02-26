#https://store.nike.com
#/html-services/gridwallData?country=CN&lang_locale=zh_CN&gridwallPath=n/1j7&pn=10
#下次响应数据在json中,所有数据从json中获取

import urllib.request
import csv
import json

    
dynamicurlroot='https://store.nike.com'
dynamicurl='https://store.nike.com/html-services/gridwallData?country=CN&lang_locale=zh_CN&gridwallPath=n/1j7&pn=1'
    
def dynamiCrawl(dynamicurl,csv_write):  

    for i in range(100):        
        with urllib.request.urlopen(dynamicurl) as f:
            data = json.loads(f.read().decode('utf-8'))
            dataKey=data['nextPageDataService']        
            print(dataKey)            
            products=data['sections'][0]['products']
            length=len(products)
            print(length)
            # print(data['sections'][0]['products'][0])
            for i in range(0,length):
                product=products[i]
                productName=product['title']+product['subtitle']
                if product['overriddenLocalPrice']==None:
                    price=product['localPrice']
                else:
                    price=product['overriddenLocalPrice']
                productUrl=product['pdpUrl']
                # print(productName,price,productUrl)
                csv_write.writerow([productName,price,productUrl])
            if dataKey==None:
                break
            dynamicurl=dynamicurlroot+dataKey
            
def writetoCsv(filename,dynamicurl):
    out=open(filename, 'w+',encoding='gb18030',newline = '')
    csv_write=csv.writer(out)
    csv_write.writerow(['商品名称','价格','商品链接'])
    dynamiCrawl(dynamicurl,csv_write)      
        
writetoCsv('nikeStore.csv',dynamicurl)
# print(n)





