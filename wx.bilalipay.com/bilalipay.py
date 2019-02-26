from util import *
import time
import json

headers = get_headers()
headers['Cookie'] = 'tgw_l7_route=4902dc6899a4ff235811291051efe7f4; PHPSESSID=ssir0o3e0lp4jpsrqc6plc5vq2; uin=332; skey=65bc17cfa44da5146b86845e27a1867465a7ce9b84af5b28; exp=316000; username=xingwd%40hlsushi.com.cn'
headers['X-Requested-With'] = 'XMLHttpRequest'


def crawl():
    page = 1
    while True:
        url = 'http://wx.bilalipay.com/index.php?r=member/record/user&g_tk=1493447614&storename=all&starttime=2015-10-10+22%3A59%3A06&endtime=2018-10-17+22%3A59%3A06&sort=&card=4&page={}'.format(page)
        req = build_request(url, headers=headers)
        data = req.json()
        result = data['data']['list']
        f = open('./result_1', 'a',encoding='utf-8')
        for line in result:
            # print(line)
            f.write(json.dumps(line, ensure_ascii=False)+'\n')
        f.close()
        print(page,'OK')
        page += 1
        if page == 500:
            break
        

crawl()
