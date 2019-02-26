from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp

# lt=['https://jinbaohong.1688.com/page/offerlist.htm?spm=a2615.7691456.newlist.98.7feb58b2CWNKTL&showType=windows&tradenumFilter=false&sampleFilter=false&sellerRecommendFilter=false&videoFilter=false&mixFilter=false&privateFilter=false&mobileOfferFilter=%24mobileOfferFilter&groupFilter=false&sortType=wangpu_score&pageNum=',]
# url_root1='https://dmqxtoy.1688.com/page/offerlist_96911367.htm?spm=a2615.7691456.newlist.101.29ea157aMi6TDa&tradenumFilter=false&sampleFilter=false&sellerRecommendFilter=false&videoFilter=false&mixFilter=false&privateFilter=false&mobileOfferFilter=%24mobileOfferFilter&groupFilter=false&sortType=wangpu_score&pageNum='
# url_root1='https://dmqxtoy1480648284896.1688.com/page/offerlist_90101145.htm?tradenumFilter=false&sampleFilter=false&sellerRecommendFilter=false&videoFilter=false&mixFilter=false&privateFilter=false&mobileOfferFilter=%24mobileOfferFilter&groupFilter=false&sortType=wangpu_score&pageNum='
url_root1='https://dmqxtoy.1688.com/page/offerlist.htm?spm=a2615.7691456.newlist.167.67e35eeaiIPXBE&tradenumFilter=false&sampleFilter=false&sellerRecommendFilter=false&videoFilter=false&mixFilter=false&privateFilter=false&mobileOfferFilter=%24mobileOfferFilter&groupFilter=false&sortType=wangpu_score&pageNum='
cook='_csrf_token=1537943057961; cna=h9/yEVZzcBsCAXrNB8OEFnAP; JSESSIONID=t2xYdgd-GQSaYYwNgVts1vi3uB-8KTUj4R-xUw9; cookie2=13979f139a3eb43841d37d6bc89a466b; hng=CN%7Czh-CN%7CCNY%7C156; t=8464a4877acc365c142612d5c3535d73; _tb_token_=e76e553eeabb5; __cn_logon__=false; _tmp_ck_0=8DDX%2FdG7Qp4rD7%2BxIUDnt9IQQps0gXg0HxVorQnE1U9h1%2BJEDnSwTlDtAa6rnpNYZgyqZ04NLkFhoSZa62xDsmigmkh2C96Zwc3vUnWDAhJ43V6s20UdSFlrW8%2FNWLYvHlj66I9JrtQip0ZR%2BRGLKKCEOXBffuleBNW%2FlS0fLs8OnUFoyVr41%2ByFFe5lUUpWm0PqHiBd%2BiTQ%2BKt8xZ%2B19oW%2B3O9I5Fgowiwd5ki0VANNbNmhmFrqb%2Fjp9ubGsMV6YsxqeJspp5sJ2OoGdhC1HaX3ei%2BzZp7K%2F2ZEmTBCHj6Lr%2Frb4LupMxN1ER%2FNrE1Rayz%2Bf5KJZR%2FhvH7p5zFUPNE1n6nNZD6KoWyAUEbhjPQYWxDmAE23JAQ0E6hEqETG; UM_distinctid=166148de0821ae-0ff23d8e76a24-b353461-100200-166148de08414f; alicnweb=touch_tb_at%3D1537948661631; isg=BEBALzn_D6g1YfOsTPGJT6ajEc7YuyZOwdqqALrREdvqNeBfYt1bIxZPSN1Qptxr'

f1=open('dmqxtoy_f.csv','w+',newline='',encoding='gb18030')
csv_write=csv.writer(f1)
page_error=[]
for i in range(1,10000):
    print(i)
    bs_obj=mytemp.getObj(url_root1+str(i),True,cook)
    
    common=bs_obj.find('div',class_='common-column-230')
    if common==None:
        try:
            common=bs_obj.find('div',class_='no-content').get_text()
            print(page_error)
            break
        except:
            page_error.append(i)
    li_list=common.find('ul',class_='offer-list-row').find_all('li',class_='offer-list-row-offer')
    for li in li_list:
        attrS=li.find('a',class_='title-link').attrs
        title=attrS['title']
        link=attrS['href']
        row=[title,link]
        # print(row)
        csv_write.writerow(row)
    
