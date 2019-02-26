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
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6",
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

def get_next_date(current_date='2017-01-01'):
    current_date=datetime.datetime.strptime(current_date,'%Y-%m-%d')
    oneday = datetime.timedelta(days=1)
    next_date = current_date+oneday
    return str(next_date).split(' ')[0]


