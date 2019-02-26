import requests
import time
# import openpyxl
import random
import datetime
import json
import re
import csv
import os


def get_headers():
    pc_headers = {
        "X-Forwarded-For": '%s.%s.%s.%s' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    return pc_headers


def get_ie_headers():
    headers = get_headers()
    headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'
    return headers


class NetWorkError(Exception):
    pass


def build_session_request(session, url, headers=None, data=None, json_data=None, timeout=15, try_times=3):
    if headers is None:
        headers = get_headers()
    for i in range(try_times):
        try:
            if data:
                response = session.post(
                    url, data=data, headers=headers, timeout=timeout)
            elif json_data:
                headers['Content-Type'] = 'application/json'
                response = session.post(
                    url, data=json.dumps(json_data), headers=headers, timeout=timeout)
            else:
                response = session.get(url, headers=headers, timeout=timeout)
            return response
        except Exception as e:
            continue
    raise NetWorkError


def build_request(url, headers=None, data=None, json_data=None, timeout=15, try_times=3):
    if headers is None:
        headers = get_headers()
    for i in range(try_times):
        try:
            if data:
                response = requests.post(
                    url, data=data, headers=headers, timeout=timeout)
            elif json_data:
                headers['Content-Type'] = 'application/json'
                response = requests.post(
                    url, data=json.dumps(json_data), headers=headers, timeout=timeout)
            else:
                response = requests.get(url, headers=headers, timeout=timeout)
            return response
        except Exception as e:
            continue
    raise NetWorkError


# def write_to_excel(lines, filename, write_only=True):
#     excel = openpyxl.Workbook(write_only=write_only)
#     sheet = excel.create_sheet()
#     for line in lines:
#         try:
#             sheet.append(line)
#         except Exception as e:
#             print('Write to excel fail', e)
#             continue
#     excel.save(filename)


def write_to_csv(lines, filename):
    csvfile = open(filename, 'w', encoding='utf-8')
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for line in lines:
        spamwriter.writerow(line)
    csvfile.close()


def get_next_date(current_date='2017-01-01'):
    current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
    oneday = datetime.timedelta(days=1)
    next_date = current_date+oneday
    return str(next_date).split(' ')[0]


def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def load_txt(filename):
    for line in open(filename, 'r'):
        try:
            item = json.loads(line)
        except Exception as e:
            print('load txt fail', e)
            continue
        yield item


def sub_str(string, words=None, append=None):
    if words is None:
        words = ['\r', '\n', '\t', '\xa0']
    if append is not None:
        words += append
    string = re.sub('|'.join(words), '', string)
    return string


def get_proxies_abuyun():
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"
    # 代理隧道验证信息
    proxyUser = 'HR3LY43V4QOU249D'
    proxyPass = 'F89DAEA7A6C85E23'

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies
    
# header={
#     'Host': 'www.amazon.com', 
#     'Referer': 'https://www.amazon.com', 
#     'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

# }
# header={
#     ":authority":"www.amazon.com",
#     ":method":"GET",
#     ":path":"/gp/bestsellers/",
#     ":scheme":"https",
#     "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     "accept-encoding":"gzip, deflate, br",
#     "accept-language":"zh-CN,zh;q=0.9",
#     "cache-control":"max-age=0",
#     "cookie":"x-wl-uid=1dHco/VSrJUr16cnal2zhX6vpptnf4AZhcNa/loYAgQ+NsTX74UP3GaGl0clmH3emUWIHs090zfY=; session-id-time=2082787201l; session-id=134-3004528-9385933; ubid-main=132-1824970-6094049; session-token=mUNaFyPCLT56ljnF/PF0NMpsPHmbzk8zALIuu2fSSFzi6KlE0liX1gy6aizYplJ/dzb+7L2rl8PIvaoyfJmu77/v87IJ8ZznR7Dyokn7vgezwuk0o/MhmR4vyP9zDFDPr7uFyAt6hc3aq5gpfXl1BBN8mbEMHR+1xE3vSoy9Ii09aOsI3Az3CYSIhztxL9UzsMxfNFxW5ZF8BeSjaRLYL6LlKsb0DkZSRL3XnyHa8V5dZ1s9Yap9vRUJqKQLUhU8z6jtAb/FpQ4=; csm-hit=tb:4RNZBNMQ5NGHVEEG8FGR+b-4RNZBNMQ5NGHVEEG8FGR|1537281999632&adb:adblk_no",
#     "upgrade-insecure-requests":"1",
#     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
# }
def build_proxy_request(url, data=None, headers=None, json_data=None):
    for i in range(5):
        try:
            if data:
                response = requests.post(
                    url, proxies=get_proxies_abuyun(), data=data, headers=headers, timeout=15)
            elif json_data:
                headers['Content-Type'] = 'application/json'
                response = requests.post(
                    url, data=json.dumps(json_data), proxies=get_proxies_abuyun(), headers=headers, timeout=15)
            else:
                response = requests.get(
                    url, headers=headers, proxies=get_proxies_abuyun(), timeout=15)
            return response
        except Exception as e:
            if '429' in str(e):
                time.sleep(random.randint(0, 1000)/1000.0)
            continue
    raise NetWorkError
