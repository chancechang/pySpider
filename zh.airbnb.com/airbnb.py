from bs4 import BeautifulSoup
import requests
import csv
import time
import json
from urllib.error import HTTPError

cook='dbcfb34a2=treatment; 50722b35e=control; 856568311=control; fa097738a=control; 74ac46b34=control; 3d727a344=control; 57675a13f=control; aa87b1240=control; d3fba8f62=control; 89ef9df7c=control; bev=1537614604_LDPCZBR19SN2Z7Wu; affiliate=43720035; campaign=.pi0.pk15169525819_49327320019_c_12026464216; _csrf_token=V4%24.airbnb.com%24W3PrXIM7bEc%24tiTfTvdd4_xdG4yaZs_F-RgDvGEy1I2o-QkERtSYqYQ%3D; flags=268435456; _airbed_session_id=669cc66ea29cfbfefd340d2e9cdf2bd9; ca78311a6=treatment1; 5319dde5f=control; cb7c7d538=treatment; affiliate_referral_at=1537614615; last_aacb=%7B%22af%22%3A%2243720035%22%2C%22c%22%3A%22.pi0.pk15169525819_49327320019_c_12026464216%22%2C%22timestamp%22%3A1537614615%2C%22gclid%22%3A%22EAIaIQobChMIzsrqo8vN3QIVl6_sCh3DdQdqEAAYASAAEgKC7vD_BwE%22%7D; _gcl_au=1.1.793958227.1537614620; _gcl_aw=GCL.1537614621.EAIaIQobChMIzsrqo8vN3QIVl6_sCh3DdQdqEAAYASAAEgKC7vD_BwE; _ga=GA1.2.361840153.1537614621; _gid=GA1.2.1102357318.1537614621; _gac_UA-2725447-1=1.1537614621.EAIaIQobChMIzsrqo8vN3QIVl6_sCh3DdQdqEAAYASAAEgKC7vD_BwE; ftv=1537614624064; cbkp=3; sdid=; __svt=690; cache_state=0; __ssid=c019537092ad1903f4fe1a6be502aeb; jitney_client_session_id=d7c01193-7105-4449-8c77-a2c073fba773; jitney_client_session_created_at=1537617144; _user_attributes=%7B%22curr%22%3A%22USD%22%2C%22guest_exchange%22%3A1.0%2C%22device_profiling_session_id%22%3A%221537614604--ebb38b444974f6aab8233e6b%22%2C%22giftcard_profiling_session_id%22%3A%221537618628--c0d2add2ea7c83b2dc815467%22%2C%22reservation_profiling_session_id%22%3A%221537618628--d0303ce2b8525b3daf142b0e%22%7D; AMP_TOKEN=%24NOT_FOUND; jitney_client_session_updated_at=1537619803'

headers = {
    "Cookie":cook,
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}


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
    return None
def getObj(url,proxyIs=False,cook=None,encode='utf-8'):
    for i in range(5):
        try:
            if cook==None:
                if proxyIs==False:
                    html=requests.get(url)
                else:
                    html=util.build_proxy_request(url)
            else:
                if proxyIs==False:
                    html=requests.get(url,headers=getHeaders(cook))
                else:
                    html=util.build_proxy_request(url)
            html.encoding=encode  
            break
        except HTTPError as e:
            # time.sleep(3)
            print('再次请求')
            print('HTTPError')
            return None
    return html

def get_profile(url):
    html=getObj(url)
    try:
        bsObj = BeautifulSoup(html.text,'html.parser')
    except AttributeError as e:
        print('AttributeError')
        return None
    try:
        profile = bsObj.find('div',class_='col-lg-9 col-md-8 col-sm-12').find('div',class_='space-top-2',recursive=False).get_text()
        return profile
    except AttributeError as e:
        print('AttributeError')
        return None
def get_review(url,type):
    html=getObj(url)
    div_data=json.loads(html.text)['review_content']
    if div_data=='':
        return []
    review_list=[]
    try:
        bsObj = BeautifulSoup(div_data,'html.parser')
        divlist=bsObj.find_all('div',class_='row text-center-sm')
        for div in divlist:
            review=div.find('div',class_='expandable-content').find('p').get_text()
            date=div.find('span',class_='text-muted date hide-sm pull-left').find('span').get_text().split('·')
            if len(date)>1:
                date=date[1]
            else:
                date=''
            review_list.append(type+date+'&nbsp;&nbsp;&nbsp'+review)
        
    except AttributeError as e:
        print('AttributeError')
        return None
    return review_list

user_url_root='https://zh.airbnb.com/users/show/'
review_root='https://zh.airbnb.com/users/review_page/'
page_host='?page='
host_root='&role=host'
guest_root='&role=guest'

# get_profile('https://zh.airbnb.com/users/show/13944258' )
# get_review(review_root+'13944258'+page_host+'1'+host_root)

filename='bj_rw_sample.csv'
csv_write=csv.writer(open('airbnb.csv','w+',newline='',encoding='gb18030'))
with open(filename,encoding='utf_8') as f:
    reader = csv.reader(f)
    rd=next(reader,None)
    for row in reader:
        review_id=row[4]
        # review_id='13944258'
        user_url=user_url_root+review_id
        profile=get_profile(user_url)
        total_review_list=[]
        page=1
        while True:
            rew_list=get_review(review_root+review_id+page_host+str(page)+host_root,'from host')
            if rew_list==[]:
                break
            total_review_list+=rew_list
            page=page+1
        page=1
        while True:
            rew_list=get_review(review_root+review_id+page_host+str(page)+guest_root,'from guest')
            if rew_list==[]:
                break
            total_review_list+=rew_list
            page=page+1
        print(row+total_review_list)
        csv_write.writerow(row+total_review_list)
        # break

