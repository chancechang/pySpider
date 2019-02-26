from bs4 import BeautifulSoup
import requests
import csv
import time

#2018年以来谷歌学术关于网络爬虫的论文
cook='NID=127=NpUXpvnAcVqGWvfYgaDn6sdKHBnk-QWTxD7H05Zmj5iPQ8j25wGD3TZq0SDbwy5L-IREwAzWWDvwyEudzqow6cn26UWwTx0qWpWSTb0d4jgdRBmwsmNsk7ka5lj8kHQ9; GSP=LM=1522932836:S=PT0o0jpvf6yxnAVf; xid=568764e87b75793244e9b39ffb2756bf; Hm_lvt_0f47b9feac1b36431493d82d708e859a=1533004860; Hm_lpvt_0f47b9feac1b36431493d82d708e859a=1533004970'
headers = {
    "Cookie":cook,
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

def getObj(url):
    try:
        html=requests.get(url,headers=headers,timeout=10)
        html.encoding="UTF-8" 
    except HTTPError as e:
        print('HTTPError')
        return None
    try:
        bsObj = BeautifulSoup(html.text,'html.parser')
    except AttributeError as e:
        print('AttributeError')
        return None
    return bsObj

def crawl(url,csv_write):
    bsObj=getObj(url)
    divlist=bsObj.find('div',{'id':'gs_res_ccl_mid'}).find_all('div',class_='gs_ri')
    print('该页面文章个数为'+str(len(divlist)))
    for div in divlist:
        url=''
        try:
            a=div.find('h3').find('a')
            title=a.get_text()
            url=a.attrs['href']
        except:
            title=div.find('h3').get_text()
        yearin=div.find('div',class_='gs_a').get_text()
        spli=yearin.find('201')
        year=yearin[spli:spli+4]
        csv_write.writerow([title,url,year])
        print(title,url,year)

urlroot1='https://xues.glgoo.com/scholar?start='
urlroot2='&q=网络爬虫&hl=zh-CN&as_sdt=0,5&as_ylo=2018'
f=open('glgoo.csv','w+',newline='',encoding='gb18030')
csv_write=csv.writer(f)
# csv_write.writerow(['标题','链接','年份'])
for i in range(0,28):
    newUrl=urlroot1+str(i*10)+urlroot2
    print('即将爬取第'+str(i)+"页,链接为"+newUrl)
    crawl(newUrl,csv_write)
    time.sleep(20)