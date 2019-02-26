from util import *
from bs4 import BeautifulSoup
import threading
import json
import os

def get_article_list(url):
    req = build_request(url)
    table = BeautifulSoup(req.text, 'lxml').find(
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
            if url[0] == '/':
                url = 'http://guba.eastmoney.com'+url
            else:
                url = 'http://guba.eastmoney.com/'+url
            pub_date = item.find('span', {'class': 'l6'}).get_text()
            view_num = item.find('span', {'class': 'l1'}).get_text()
            review_num = item.find('span', {'class': 'l2'}).get_text()
            result.append([title, url, pub_date, view_num, review_num])
        except:
            continue
    return result


def get_article_info(url):
    req = build_request(url)
    zwcontent = BeautifulSoup(req.text, 'lxml').find(
        'div', {'id': 'zwcontent'})
    pub_time = zwcontent.find('div', {'class': 'zwfbtime'}).get_text()
    content = zwcontent.find('div', {'id': 'zwconbody'}).get_text()
    return [pub_time, content]


class ArticleInfo(threading.Thread):
    def __init__(self, item):
        super(ArticleInfo, self).__init__()
        self.item = item
        self.url = self.item[1]
        self.daemon = True

    def run(self):
        self.status = False
        try:
            info = get_article_info(self.url)
            self.result = self.item+info
            self.status = True
        except Exception as e:
            return


def crawl():
    try:
        os.mkdir('files')
    except:
        pass
    code = 'zssh000001'
    page = 1
    pre_list = []
    while True:
        url = 'http://guba.eastmoney.com/list,{},f_{}.html'.format(code, page)
        try:
            art_list = get_article_list(url)
        except Exception as e:
            print(url, 'Failed', e)
            break
        if art_list == pre_list:
            break
        pre_list = art_list
        tasks = []
        for item in art_list:
            task = ArticleInfo(item)
            tasks.append(task)
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()
        result_f = open('./files/%s.txt' % code, 'a', encoding='utf-8')
        for task in tasks:
            if task.status:
                result_f.write(json.dumps(task.result)+'\n')
            else:
                with open('./files/%s_failed.txt' % code, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(task.item)+'\n')
        result_f.close()
        print(url, 'OK')
        page += 1


crawl()
