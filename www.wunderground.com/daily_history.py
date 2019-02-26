from util import *
from bs4 import BeautifulSoup
import time
import json

def get_daily_history(city_code='ZHHH', date='2017-01-01'):
    year = date.split('-')[0]
    month = int(date.split('-')[1])
    day = int(date.split('-')[-1])
    url = 'https://www.wunderground.com/history/airport/{}/{}/{}/{}/DailyHistory.html'.format(
        city_code, year, month, day)
    req = build_request(url)
    table = BeautifulSoup(req.text, 'lxml').find(
        'table', {'id': 'obsTable'}).find('tbody').find_all('tr')
    result = {}
    for tr in table:
        td_list = tr.find_all('td')
        line = []
        for td in td_list:
            value = td.get_text().replace('\r', '').replace(
                '\n', '').replace('\xa0', ' ').replace('\t', ' ')
            line.append(value)
        hour = int(line[0].split(':')[0])
        is_am = True
        if 'PM' in line[0]:
            is_am=False
        if is_am:
            if hour==12:
                current_time=date+' '+'00:00:00'
            else:
                current_time=date+' '+'%02d:00:00'%(hour)
        else:
            if hour==12:
                current_time=date+' '+'12:00:00'
            else:
                current_time=date+' '+'%02d:00:00'%(hour+12)
        result[current_time]=[current_time]+line
    air_report=[]
    for key in result:
        air_report.append(result[key])
    return air_report

def crawl():
    current_date='2014-05-01'
    while current_date!='2017-12-01':
        result=get_daily_history('ZHHH',current_date)
        f=open('./result.txt','a')
        for line in result:
            f.write(json.dumps(line)+'\n')
        f.close()
        print(current_date,'OK')
        current_date=get_next_date(current_date)


def load_txt():
    for line in open('./result.txt','r'):
        item=json.loads(line)
        item[-5]=item[-5].split(' /')[0]
        if len(item)==13:
            item=item[:3]+['']+item[3:]
        yield item

write_to_excel(load_txt(),'result.xlsx')
