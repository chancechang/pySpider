#动态加载
#the commuter
#http://m.imdb.com/title/tt1590193/reviews?ref_=m_tt_urv
#the 15:17 to Paris

from bs4 import BeautifulSoup
import requests
import csv



def build_request(url):
    for i in range(5):
        try:
            req=requests.get(url,timeout=20)
            return req
        except:
            continue
    return None
    
url1='http://m.imdb.com/title/tt1590193/reviews?ref_=m_tt_urv'
dynamicurl1='http://m.imdb.com/title/tt1590193/reviews/_ajax?ref_=undefined&paginationKey='
url2='http://m.imdb.com/title/tt6802308/reviews?ref_=m_tt_urv'
dynamicurl2='http://m.imdb.com/title/tt6802308/reviews/_ajax?ref_=undefined&paginationKey='

    
def crawl(url,dynamicurl,csv_write):  
    req=build_request(url)
    req.encoding='utf-8'
    soup=BeautifulSoup(req.text,'html.parser')
    reviews=soup.find('div', {'id': 'reviews-container'}).find_all('li',class_='ipl-content-list__item')
    for review in reviews:
        userName=review.find('span',class_='display-name-link').string
        time=review.find('span',class_='review-date').string
        if review.find('span',class_='rating-other-user-rating'):
            score=review.find('span',class_='rating-other-user-rating').find('span').string+'.0 / 10'
        else:
            score=''
        title=review.find('span',class_='title').string
        
        if review.find('span',class_='spoiler-warning__control ipl-expander__control'):
            text=review.find('span',class_='spoiler-warning__control ipl-expander__control').string
        else:
            text=review.find('div',class_='text').get_text()
        print(score,title,userName,time)
        csv_write.writerow([score,title,userName,time,text])
    if soup.find('div',class_='load-more-data'): 
        dataKey=soup.find('div',class_='load-more-data')['data-key']
        print(dataKey)
        crawl(dynamicurl+dataKey,dynamicurl,csv_write)

def writetoCsv(filename,url,dynamicurl):
    out=open(filename, 'w+',encoding='gb18030',newline = '')
    csv_write=csv.writer(out)
    csv_write.writerow(['评分','评论题目','用户名','时间','评论内容'])
    crawl(url,dynamicurl,csv_write)      
        
writetoCsv('imdbcommuter.csv',url1,dynamicurl1)
writetoCsv('imdbparis.csv',url2,dynamicurl2)



