from bs4 import BeautifulSoup
import requests
import time
import openpyxl
import random
import datetime

def get_headers():
    pc_headers = {
        "X-Forwarded-For": '%s.%s.%s.%s' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }
    return pc_headers


class NetWorkError(Exception):
    pass


def build_request(url, headers=None):
    if headers is None:
        headers = get_headers()
    for i in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            return response
        except:
            continue
    raise NetWorkError

def write_to_excel(lines,filename,write_only=True):
    excel=openpyxl.Workbook(write_only=write_only)
    sheet=excel.create_sheet()
    for line in lines:
        sheet.append(line)
    excel.save(filename)


def parser_html(html):
    soup=BeautifulSoup(html,'html.parser')
    reviews=soup.find('div', {'id': 'reviews-container'}).find_all('li',class_='ipl-content-list__item')

    result=[]
    for review in reviews:
        userName=review.find('span',class_='display-name-link').string
        time=review.find('span',class_='review-date').string
        if review.find('span',class_='rating-other-user-rating'):
            score=review.find('span',class_='rating-other-user-rating').get_text().replace('\n','')
        else:
            score=''
        title=review.find('span',class_='title').string
        text=review.find('div',class_='text').get_text()
        line=[userName,time,title,score,text]
        result.append(line)
    return result

def get_data_key(html):
    soup=BeautifulSoup(html,'html.parser').find('div',{'class':'load-more-data'})
    if soup is None:
        return None
    return soup.get('data-key')


def crawl(movie_code,filename):
    start_url='http://m.imdb.com/title/{}/reviews?ref_=m_tt_urv'.format(movie_code)
    req=build_request(start_url)
    result=parser_html(req.text)
    data_key=get_data_key(req.text)
    print(data_key)
    while data_key:
        url='http://m.imdb.com/title/{}/reviews/_ajax?ref_=undefined&paginationKey={}'.format(movie_code,data_key)
        req=build_request(url)
        result+=parser_html(req.text)
        data_key=get_data_key(req.text)
        print(data_key)
    write_to_excel(result,filename)

crawl('tt1590193','imdb_commuter.xlsx')
crawl('tt6802308','imdb_paris.xlsx')
