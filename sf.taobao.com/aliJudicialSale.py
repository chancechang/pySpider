import requests
import urllib.request
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from selenium import webdriver
import time
import json
import csv
import re
from math import ceil

cook='thw=cn; cna=h9/yEVZzcBsCAXrNB8OEFnAP; t=958b680ed770b65bab4bb2b433356b70; hng=CN%7Czh-CN%7CCNY%7C156; enc=winkIkIUm01cbE9wGg4OyAkUlZEWKizvTz7i80i2Blb9Fv2UQ8qEYL9YVPSN0X6hoAeV3%2BJOJXQLJjkPMQ%2BsbA%3D%3D; v=0; cookie2=1b4bdb85b9f4d47b863f60df99dd5066; _tb_token_=5bee83eeeebf4; uc1=cookie14=UoTeOoncvBuR0A%3D%3D; isg=BJqaMZQulE3sCRtDdFyEQh7t60C2x1MylzhA3qQTRi34FzpRjFtutWBl4-OL3JY9'
headers = {
    "Cookie":cook,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept - Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    # 'Connection':'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',}

def getObj(url):
    try:
        html=requests.get(url,headers=headers)
        html.encoding="gb2312"
    except HTTPError as e:
        print('HTTPError')
        return None
    try:
        bsObj = BeautifulSoup(html.text,'html.parser')
    except AttributeError as e:
        print('AttributeError')
        return None
    return bsObj

def stampToLocal(t):
    time_local=time.localtime(t/1000)
    return  (time.strftime("%Y-%m-%d %H:%M:%S",time_local))

def crawl(url):
    bsObj=getObj(url)
    data=json.loads(bsObj.find('script',{'id':'sf-item-list-data'}).get_text())['data']
    for li in data:
        status=li['status']
        title=li['title']
        link=li['itemUrl']
        start=li['start']
        # end=li['end']
        # currentPrice=li['currentPrice']
        # delayCount=li['delayCount'] #延时次数
        # bidCount=li['bidCount'] #竞价次数
        # applyCount=li['applyCount']   #报名人数
        # viewerCount=li['viewerCount'] #围观人数
        if status=='done':
            f1.write(str([title,link,start])+'\n')
        else: 
            pass
            # f2.write(str([title,link,status])+'\n')

def write(title,text,result):
    for i in range(2):
        try:
            t=headlist.index(title)
            result[t]=text
            break
        except:
            headlist.append(title)
    return result

def detailCrawl(line,url):
    if len(headlist)<=28:
        n=30
    else:
        n=len(headlist)+3

    bsObj=getObj(url)
    module1=bsObj.find('div',class_='pm-main clearfix')
    aucTime=module1.find('h1').get_text().strip()[1:].split("】")[0]
    if aucTime.find('拍卖')>=2:
        result=['' for i in range(n)]
        result[0]=line[0]
        result[1]=url
        result[2]=line[2]
        result=write("开始时间",stampToLocal(int(line[2])),result)
        result=write("第几次拍卖",aucTime,result)
        right=module1.find('div',class_='pm-main-l auction-interaction')
        #成交价
        rp=right.find("li",{'id':'sf-price'})
        rpTitle=rp.find('span',class_='title').get_text().strip()
        rpText=rp.find('span',class_="pm-current-price J_Price").get_text().strip().replace(",","")
        result=write(rpTitle,rpText,result)
        #成交时间
        rtTitle=right.find('span',class_='title over-title').get_text().strip()
        rtText=right.find('span',class_='countdown J_TimeLeft').get_text().strip()
        result=write(rtTitle,rtText,result)
        #延时次数
        delayCnt=right.find('span',{'id':'J_Delay'}).find('em',class_='delayCnt').get_text().strip()
        result=write('延时次数',delayCnt,result)
        #起拍价，保证金...
        rtdlist=right.find('tbody',{'id':'J_HoverShow'}).find_all('td')
        for td in rtdlist:
            splist=td.find_all('span')
            if len(splist)>=2:
                result=write(splist[0].get_text().replace(" ",""),re.sub("\n| ","",splist[1].get_text().strip().replace(":","").replace("¥","￥")),result)
        #预计结束时间
        try:
            period=result[13].find('天')
            estEndT=stampToLocal(int(result[13][:period])*24*3600*1000+line[2])
        except:
            period=result[13].find('周')
            estEndT=stampToLocal(int(result[13][:period])*24*3600*1000*7+line[2])
        result=write('预计结束时间',estEndT,result)
        # weeks=result[13].find('周')
        # days=result[13].find('天')
        # hours=result[13].find('小时')
        # estTime=line[2]
        # t=0
        # if weeks>0:
        #     estTime+=int(result[13][t:weeks])*24*3600*1000*7
        #     t=weeks+1
        # if days>0:
        #     estTime+=int(result[13][t:days])*24*3600*1000
        #     t=days+1
        # if hours>0:
        #     estTime+=int(result[13][t:hours])*3600*1000
        # estEndT=stampToLocal(estTime)
        # result=write('预计结束时间',estEndT,result)
        #处置单位
        pai_info_list=right.find('div',class_='pai-info').find_all('p')
        for p in pai_info_list:
            p=re.sub("\n|\t","",p.get_text()).strip()
            if p.find('处置单位')>=0:
                result=write('处置单位',p.replace("处置单位：",""),result)

        #"报名人数","设置提醒人数","围观次数"
        pm_remind=module1.find('div',class_='pm-remind')
        result=write("报名人数",pm_remind.find("em",class_='J_Applyer').get_text(),result)
        result=write("设置提醒人数",pm_remind.find("span",class_='pm-reminder i-b').find('em').get_text(),result)
        result=write("围观次数",pm_remind.find("em",{'id':'J_Looker'}).get_text(),result)
        
        module2=bsObj.find('ul',{"id":'J_DetailTabMenu'})
        J_Record=re.sub("\n|\t","",module2.find('span',class_='J_Record').get_text())
        result=write("竞买次数",J_Record,result)

        # recordTable=bsObj.find("div",{'id':"J_RecordContent"}).attrs['data-from']
        # print(recordTable)
        # //sf.taobao.com/json/get_bid_records.htm?id=566824980294&records_type=pageRecords




    else:
        f3.write(str([aucTime,line[0],url])+'\n')
        return
    
    print(result)
    # csv_write.writerow(result)

def getJson(url):
    #获取json
    f= urllib.request.Request(url,headers=headers)
    data=urllib.request.urlopen(f).read().decode('utf-8',"ignore")
    return data

def crawlRecord(url):
    result=[]
    aliasList=re.findall('alias:"(.*?)"',getJson(url))
    dateList=re.findall('date:"(.*?)"',getJson(url))
    priceList=re.findall('price:"(.*?)"',getJson(url))
    for i in range(len(aliasList)):
        result.append(aliasList[i])
        result.append(dateList[i])        
        result.append(priceList[i].replace(",",""))
        
    return result

# urlRoot='https://sf.taobao.com/list/50025972__2.htm?spm=a213w.7398504.pagination.1.OYOdff&auction_start_seg=-1&page='

# f1=open('alisalelistd.txt','w',encoding='gb18030') 
# f2=open('alisalelistf.txt','a+',encoding='gb18030')
# for i in range(1,158):
#     print(i)
#     url=urlRoot+str(i)
#     crawl(url)
headlist=["标题","链接","开始时间","预计结束时间","第几次拍卖","成交价","成交时间","延时次数","起拍价","保证金",\
        "评估价","加价幅度","竞价周期","延时周期","类型",\
        "优先购买权人","处置单位","报名人数","设置提醒人数",\
        "围观次数","竞买次数","市场价"]

# f3=open('doneOther.txt','w+',encoding='gb18030')
# out=open('JudiSaleMotor.csv', 'w+',encoding='gb18030',newline = '')
# csv_write=csv.writer(out)
# t=1
# for line in open('alisalelistd.txt','r',encoding='gb18030'):
#     line=eval(line)
#     url='https:'+line[1]
#     print(url)
#     print(t)
#     for i in range(3):
#         try:
#             detailCrawl(line,url)
#             break
#         except:
#             if i==2:
#                 csv_write.writerow(headlist)
#                 f3.write(str(line)+'\n')
#             time.sleep(3)      
#     # if t==2:
#     #     break
#     t+=1
#     time.sleep(1)
# csv_write.writerow(headlist)



# https://sf.taobao.com/json/get_bid_records.htm?currentPage=2&id=566824980294&records_type=pageRecords
# https://sf.taobao.com/json/get_bid_records.htm?currentPage=1&id=566824980294&records_type=pageRecords

# urlRoot='https://sf.taobao.com/json/get_bid_records.htm?currentPage='
# out=open('JudiSaleFinal.csv', 'a+',encoding='gb18030',newline = '')
# csv_write=csv.writer(out)
# csv_write.writerow(headlist)

# for line in csv.reader(open('JudiSaleMotor.csv','r')):
#     if len(line)==21:
#         line.append('')
#     uId=line[1].replace("https://sf.taobao.com/sf_item/",'')[:12]
#     recordCount=ceil(int(line[20])/20)
#     for i in range(1,recordCount+1):
#         newUrl=urlRoot+str(i)+'&id='+uId+'&records_type=pageRecords'
#         for i in range(3):
#             try:
#                 record=crawlRecord(newUrl)
#                 break
#             except:
#                 if i==2:
#                     raise RuntimeError('testError')
#                 time.sleep(3)   
        
#         line=line+record
#     csv_write.writerow(line)
#     time.sleep(10)

# out=open('JudiSaleReasonable.csv', 'w+',encoding='gb18030',newline = '')
# csv_write=csv.writer(out)
# csv_write.writerow(headlist)
# for line in csv.reader(open('JudiSaleMotorFinal.csv','r')):
#     if line[5]=='成交价':
#         continue
#     if len(line)==21:
#         line.append('')
#     if float(line[5])/float(line[8].replace("￥",'').replace(',',''))<10:
#         csv_write.writerow(line)

# out1=open('.\\JudiSaleReaFinal.csv', 'w+',encoding='gb18030',newline = '')
# csv_write1=csv.writer(out1)
# csv_write1.writerow(headlist+['竞买记录','跳跃记录'])
for line in csv.reader(open('JudiSaleReasonable.csv','r')):
    if line[5]=='成交价':
        continue
    writer=line[:22]
    uId=line[1].replace("https://sf.taobao.com/sf_item/",'')[:12]
    out2=open('.\\data\\'+uId+'.csv', 'w+',encoding='gb18030',newline = '')
    csv_write2=csv.writer(out2)
    out3=open('.\\data\\'+uId+'jump.csv', 'w+',encoding='gb18030',newline = '')
    csv_write3=csv.writer(out3)
    
    raiserange=float(line[11].replace("￥",'').replace(',',''))
    newdata=[0 for t in range(12)]
    for i in range(22,len(line),3):
        #计算时机,时间戳以秒为单位
        starttime=int(time.mktime(time.strptime(line[2],"%Y/%m/%d %H:%M")))
        planovertime=int(time.mktime(time.strptime(line[3],"%Y/%m/%d %H:%M")))
        if line[i+1]=='':
            break
        # print(line[i+1])
        timenow=int(time.mktime(time.strptime(line[i+1],"%Y%m%d %H:%M:%S")))
        #时机
        usefulTime=float(timenow-starttime)/(planovertime-starttime)
        csv_write2.writerow([line[i],line[i+2],line[i+1],usefulTime])
        if i+5>len(line):
            break
        if line[i+5]=='':
            break
        jump=float(line[i+2])-float(line[i+5])-raiserange
        if jump>0:
            csv_write3.writerow([line[i],jump,usefulTime])
            newdata[0]+=jump
            newdata[1]+=1
            
            if usefulTime<0.5:
                newdata[3]+=jump
                newdata[4]+=1
            elif usefulTime<1-300/(planovertime-starttime):
                newdata[6]+=jump
                newdata[7]+=1
            else:
                newdata[9]+=jump
                newdata[10]+=1

    for j in range(0,12,3):
        if newdata[j+1]==0:
            continue
        newdata[j+2]=float(newdata[j])/newdata[j+1]
    # writer+=newdata
    # writer.append('.\\data\\'+uId+'.csv')
    # writer.append('.\\data\\'+uId+'jump.csv')
    # csv_write1.writerow(writer)
    
    out2.close()
    out3.close()


    

# =HYPERLINK(JD5,JD5)

