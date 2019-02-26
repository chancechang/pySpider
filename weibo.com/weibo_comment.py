from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
import time
import json
import re
import xlsxwriter

f=open('lenovo_comment.txt','w+',encoding='utf-8')
i=1
while True:
    print(i)
    #评论
    url='https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4240258017111253&root_comment_max_id_type=0&root_comment_ext_param=&page='+str(i)+'&filter=hot&filter_tips_before=1&from=singleWeiBo'
    #转发
    # url='https://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=4240258017111253&max_id=4299801228700542&page='+str(i)
    cook='SINAGLOBAL=1000991548225.687.1501208801677; UOR=,,bookshadow.com; YF-Page-G0=f70469e0b5607cacf38b47457e34254f; SUB=_2AkMssHxdf8NxqwJRmPATzGnnaYRwzwnEieKa7I2GJRMxHRl-yj83qlEFtRB6BzBSsVXhYFlmooa4wOsMyKJlHBrWFC8X; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5kqUa2MwHrFB1UIrO4ZSQA; _s_tentry=passport.weibo.com; Apache=7722774755339.894.1542255473619; ULV=1542255473994:3:1:1:7722774755339.894.1542255473619:1521984742062; Ugrow-G0=e66b2e50a7e7f417f6cc12eec600f517; YF-V5-G0=2a21d421b35f7075ad5265885eabb1e4'
    header={
        'Referer':'https://weibo.com/2183473425/GgTihtPXD?from=page_1006062183473425_profile&wvr=6&mod=weibotime&type=comment',
        # 'Referer':'https://weibo.com/2183473425/GgTihtPXD?from=page_1006062183473425_profile&wvr=6&mod=weibotime&type=repost',       
        'Cookie':cook
    }
    req=requests.get(url,headers=header)
    html=json.loads(req.text)['data']['html']
    bsObj=BeautifulSoup(html,"html.parser")
    com_list=bsObj.find_all('div',class_='list_li S_line1 clearfix')
    for com in com_list:
        com_peo=com.find('div',class_='WB_text')
        a=com_peo.find('a')
        href=a.attrs['href']
        usercard=a.attrs['usercard']
        name=a.get_text()
        com_text=com_peo.get_text().strip()
        time=com.find('div',class_='WB_from S_txt2').get_text()
        recall=com.find('div',class_='list_li_v2')
        # print(recall.get_text())
        if recall!=None:
            # print('daoda')
            try:
                recall_text=recall.get_text()
                recall_num=re.search(r'共(.+?)条回复',recall_text).group(1)
                # print(recall_num)
            except:
                recall_num=0
        else:
            recall_num=0
        zan_num=com.find('div',class_='WB_handle W_fr').find_all('em')[-1].get_text()
        row=[href,usercard,name,com_text,time,recall_num,zan_num]
        f.write(str(row)+'\n')
    # com_list=bsObj.find_all('div',class_='list_li S_line1 clearfix')
    # for com in com_list:
    #     com_peo=com.find('div',class_='WB_text')
    #     a=com_peo.find('a')
    #     href=a.attrs['href']
    #     usercard=a.attrs['usercard']
    #     name=a.get_text()
    #     com_text=com_peo.get_text().strip()
    #     time=com.find('div',class_='WB_from S_txt2').find('a').attrs['title']
    #     num_set=com.find('div',class_='WB_handle W_fr').find_all('li')
    #     recall_num=num_set[-2].get_text().replace('\n','')
    #     zan_num=num_set[-1].get_text().replace('\n','')
    #     row=[href,usercard,name,com_text,time,recall_num,zan_num]
    #     print(row)
    #     f.write(str(row)+'\n')
    i=i+1
    # break
f.close()
filename='联想事件评论'
workbook=xlsxwriter.Workbook(filename+'.xlsx')
sheet=workbook.add_worksheet()
i=0
for line in open('lenovo_comment.txt','r',encoding='utf-8'):
    line=eval(line)
    line[3]=line[3].replace(line[2]+'：','')
    if '赞' in line[-1]:
        line[-1]=0
    # else:
    #     line[-1]=line[-1].replace('ñ','')
        
    # try:
    #     line[-2]=line[-2].replace('转发','').strip()
    # except:
    #     print(line[-2])
    # if line[-2]=='':
    #     line[-2]=0
    # print(line)
    for t in range(len(line)):
        sheet.write(i,t,line[t])
    i=i+1
    # break

workbook.close() 


# header={
#     'Referer':'https://gitter.im/ethereum/go-ethereum/~chat',
#     'Cookie':'g_session=s%3ANKuvCegJYGcUwd3h1thZrRUESuZmOv82.0Vlrnhn2%2BlGltkJF%2BBYCBIbyy0eAnH9GvsOT55yiz%2Fc; webfontsLoaded=true',
#     'x-access-token':'$MQcH3uyelKSiYeKYkn7HrqSc0EaKkpaLSkwmzMYCS1w='
# }
# url='https://gitter.im/api/v1/rooms/53e1cb8a107e137846ba97c2/users?limit=250'
# req=requests.get(url,headers=header)
# print(req.text)


#      com_list=bsObj.find_all('div',class_='list_li S_line1 clearfix')
#     for com in com_list:
#         com_peo=com.find('div',class_='WB_text')
#         a=com_peo.find('a')
#         href=a.attrs['href']
#         name=a.get_text()
#         com_text=com_peo.get_text().strip()
#         time=com.find('div',class_='WB_from S_txt2').get_text()
#         recall=com.find('div',class_='list_li_v2')
#         # print(recall.get_text())
#         if recall!=None:
#             # print('daoda')
#             try:
#                 recall_text=recall.get_text()
#                 recall_num=re.search(r'共(.+?)条回复',recall_text).group(1)
#                 # print(recall_num)
#             except:
#                 recall_num=0
#         else:
#             recall_num=0
#         zan_num=com.find('div',class_='WB_handle W_fr').find_all('em')[-1].get_text()
#         row=[href,name,com_text,time,recall_num,zan_num]