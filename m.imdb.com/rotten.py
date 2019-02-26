#https://www.rottentomatoes.com/m/the_commuter/reviews/
#https://www.rottentomatoes.com/m/the_1517_to_paris/reviews/




from bs4 import BeautifulSoup
import requests
import csv


root1='https://www.rottentomatoes.com/m/the_commuter/reviews/?page='
root2='https://www.rottentomatoes.com/m/the_1517_to_paris/reviews/?page='



def build_request(url):
    for i in range(5):
        try:
            req=requests.get(url,timeout=20)
            return req
        except:
            continue
    return None

def crawl(root,filename,num):
    
    out1=open(filename, 'w+',encoding='gb18030',newline = '')
    csv_write1=csv.writer(out1)
    csv_write1.writerow(['评分','评论题目','用户名','时间','评论内容'])

    for i in range(1,num+1):
        url=root+str(i)+'&sort='
        req=build_request(url)
        req.encoding='utf-8'
        soup=BeautifulSoup(req.text,'html.parser')
        reviews=soup.find('div', class_='review_table').find_all('div',class_='row review_table_row')
        for review in reviews:
            userName=review.find('a',class_='unstyled bold articleLink').string
            time=review.find('div',class_='review_date subtle small').string
            if review.find('div',class_='small subtle').get_text().find(':' )!=-1:
                score=review.find('div',class_='small subtle').get_text().split(':')[-1]
            else:
                score=''
            # title=review.find('span',class_='the_review').string
            text=review.find('div',class_='small subtle').find('a')['href']
            print(userName,time,score)
            csv_write1.writerow([score,'',userName,time,text])

crawl(root1,'rottencommuter.csv',9)
crawl(root2,'rottenparis.csv',7)
