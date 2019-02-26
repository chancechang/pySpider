from bs4 import BeautifulSoup
import requests
import csv
import sys
sys.path.append("..")
import mytemp
import util
url='https://www.ebay.com/b/Toys-Hobbies/220/bn_1865497?rt=nc&LH_BIN=1&LH_PrefLoc=6&rt=nc&_pgn='

def getlink():

    f=open('ebay_toys.csv','w+',newline='',encoding='gb18030')
    csv_write=csv.writer(f)
    f1=open('log.txt','w+')
    for i in range(1,100):
        newUrl=url+str(i)
        for j in range(5):
            try:
                req=util.build_proxy_request(newUrl)
                bsObj=BeautifulSoup(req.text,'html.parser')
                lilist=bsObj.find('ul',class_='b-list__items_nofooter').find_all('li')
                break
            except:
                pass
            if j==4:
                #该页取不到数据
                f1.writelines(str(i)+'\n')
                lilist=[]

        for li in lilist:
            name=''
            the_url=''
            watch_sold=''
            location=''
            try:
                name=li.find('h3',class_='s-item__title').get_text()
                the_url=li.find('a',class_='s-item__link').attrs['href']
            except:
                pass
            try:
                watch_sold=li.find('span',class_='NEGATIVE').get_text()
            except:
                pass
            try:
                location=li.find('span',class_='s-item__location s-item__itemLocation').get_text()     
            except:
                pass
            row=[name,the_url,watch_sold,location]
            print(row)
            csv_write.writerow(row)

def crawl(url):
    f3=open('logrwid.txt','w+')
    review=[]
    for j in range(5):
        try:
            req=util.build_proxy_request(url)
            bsObj=BeautifulSoup(req.text,'html.parser')
            # print(bsObj)
            body=bsObj.find('div',{'id':'BottomPanelDF'})            
            break
        except:
            pass
        if j==4:
            #该页取不到数据
            f3.writelines(url+'\n')
    try:
        divlist=body.find('div',{'id':'rwid'}).find_all('div',class_=' ebay-review-section')
    except:
        return []

    for div in divlist:
        title=''
        content=''
        try:
            title=div.find('p',class_='review-item-title wrap-spaces').get_text()
        except:
            pass
        try:
            content=div.find('p',class_='review-item-content wrap-spaces').get_text()
        except:
            pass
        review.append(title+':::'+content)
    return review

f_read=open('ebay_toys_filter.csv','r',encoding='gb18030')
f2=open('reviews.csv','w+',encoding='gb18030')
csv_write1=csv.writer(f2)
num=0
for line in csv.reader(f_read):
    print(line[1])
    reviews=crawl(line[1])
    num=num+len(reviews)

    csv_write1.writerow(line+reviews)
print(num)
