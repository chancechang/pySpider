#http://guba.eastmoney.com/list,zssh000001_1.html

from bs4 import BeautifulSoup
import requests
import csv
import threading
from log import info_logger


def build_request(url):
    for i in range(5):
        try:
            req=requests.get(url,timeout=20)
            return req
        except:
            continue
    return None

root='http://guba.eastmoney.com/'
root1='list,zssh000001_'
out=open('dfcfgbtest1.csv', 'w+',encoding='gb18030',newline = '')
csv_write=csv.writer(out)
csv_write.writerow(['评论数','阅读数','时间','标题','内容'])


def crawl(pagenum,sum):
    if pagenum>sum:
        return
    req=build_request(root+root1+str(pagenum)+'.html')
    req.encoding='utf-8'
    soup=BeautifulSoup(req.text,'html.parser')
    articallist=soup.find_all('div',class_='articleh')
    # print(len(articallist))
    # if len(articallist)<80:
    #     print('重新爬取第'+str(pagenum)+'页')
    #     print('网址：'+root+root1+str(pagenum)+'.html')
    #     return crawl(pagenum,sum)
    for i in range(0,len(articallist)):
        if len(articallist[i].find_all('span'))<3:
            # print(articallist[i])
            continue
        readNum=articallist[i].find('span',class_='l1').string
        commentNum=articallist[i].find('span',class_='l2').string
        title=articallist[i].find('span',class_='l3').find_all('a')[-1].string
        url=articallist[i].find('span',class_='l3').find_all('a')[-1]['href'].replace('/','')
               
        # print(root+url)
        req1=build_request(root+url)
        req1.encoding='utf-8'
        soup1=BeautifulSoup(req1.text,'html.parser')
        # print(soup1.find('div',class_='zwfbtime'))
        if soup1.find('div',class_='zwfbtime')==None:
            continue
        publishTime=soup1.find('div',class_='zwfbtime').string.split(' ')[1]        
        if publishTime.find('2017')==0:
            if soup1.find('div',{'id':'zw_body'}):
                content=soup1.find('div',{'id':'zw_body'}).get_text()       
            else:
                content=soup1.find('div',class_='stockcodec').get_text()
            if publishTime.find('2017')==0:
                print(commentNum,readNum,publishTime,title)
                csv_write.writerow([commentNum,readNum,publishTime,title,content])
    pagenum=pagenum+1
    print('即将开始爬取第'+str(pagenum)+'页')
    return crawl(pagenum,sum)


crawl(50,6899)
def get_article_list(url):
    req = build_request(url)
    res_text = req.text
    table = BeautifulSoup(res_text, 'lxml').find(
        'div', id='articlelistnew').find_all('div', {'class': 'articleh'})
    result = []
    for item in table:
        try:
            l3 = item.find('span', {'class': 'l3'})
            try:
                hinfo = item.find('em').get_text()
                if hinfo in ['新闻', '大赛', '公告', '研报']:
                    continue
            except:
                pass
            title = l3.find('a').get_text()
            url = l3.find('a').get('href')
            pub_date = item.find('span', {'class': 'l6'}).get_text()
            result.append([title, url, pub_date])
        except:
            continue
    return result


class GubaArticleList(threading.Thread):
    def __init__(self, base_info):
        super(GubaArticleList, self).__init__()
        self.base_info = base_info
        self.result = []
        self.code = base_info[-1]
        self.failed_url = []
        self.daemon = True

    def run(self):
        current_year = 2018
        pre_list = []
        page = 1
        year_state = 0
        while True:
            url = 'http://guba.eastmoney.com/list,{},f_{}.html'.format(
                self.code, page)
            try:
                art_list = get_article_list(url)
            except Exception as e:
                break
            if art_list == pre_list:
                break
            pre_list = art_list
            for item in art_list:
                pub_date = item[-1]
                if current_year == 2014 and '07-' in pub_date:
                    return
                if '01-' in pub_date:
                    year_state = 1
                if '12-' in pub_date and year_state == 1:
                    year_state = 0
                    current_year = current_year - 1
                self.result.append(self.base_info + item +
                                   ['%s-%s' % (current_year, pub_date)])
            if current_year < 2014:
                break
            page += 1


def load_codes():
    tasks = []
    for line in open('./files/codes.txt', 'r'):
        item = eval(line)
        tasks.append(item)
        if len(tasks) < 5:
            continue
        yield tasks
        tasks = []
    yield tasks


def crawl():
    for stock_list in load_codes():
        tasks = []
        for stock in stock_list:
            task = GubaArticleList(stock)
            tasks.append(task)
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
        for task in tasks:
            com_type = task.base_info[0]
            f = open('./result/%s.txt' % (com_type), 'a')
            for item in task.result:
                f.write(str(item) + '\n')
            f.close()

            failed = open('./result/failed.txt', 'a')
            for item in task.failed_url:
                failed.write(str(item) + '\n')
            failed.close()
