
import requests
import csv
import json
import time
import datetime



MAX_Page=500

headers = {
    'Referer':'http://bond.sse.com.cn/data/statistics/survey/single/',
    'Host':'query.sse.com.cn'
    }

def main(today,begin=None,end=None):
    if begin==None:
        date=today
    else:
        date=begin+'_'+end
        try:
            beginDate=datetime.datetime.strptime(begin, "%Y-%m-%d")    
            endDate=datetime.datetime.strptime(end, "%Y-%m-%d")    
        except:
            print('日期不合法，请重新输入')
            return choose()
        if beginDate>endDate:
            print('起止日期不合规范，请重新输入')
            return choose()

    urlroot='http://query.sse.com.cn/commonQuery.do?isPagination=true&sqlId=COMMON_BOND_XXPL_ZQXX_L&pageHelp.pageSize=20&BONDTYPE=%E8%AF%81%E5%88%B8%E5%85%AC%E5%8F%B8%E8%B5%84%E4%BA%A7%E6%94%AF%E6%8C%81%E8%AF%81%E5%88%B8'
    f1=open(date+'企业资产支持证券.csv','w+',encoding='gb18030',newline='')
    csv_write=csv.writer(f1)
    rowname=['序号',	'债券代码',	'债券简称',	'债券全称'	,'质押券简称','质押券代码',	'期限(年)'	,'计息方式'	,'付息方式',	'发行量(亿元)',	'上市日期'	,'发行起始日'	,'发行终止日'	,'到期日']
    csv_write.writerow(rowname)
    for i in range(1,MAX_Page,5):
        url=urlroot+'&pageHelp.pageNo='+str(i+1)+'&pageHelp.beginPage='+str(i)+'&pageHelp.endPage='+str(i+4)
        
        for i in range(5):
            try:
                bsObj=requests.get(url,headers=headers,timeout=15)
                break
            except:
                pass
        if bsObj==None:
            print('error')
            break
        data=json.loads(bsObj.text)['result']
        if len(data)==0:
            break
        
        #判断开始日期和结束日期
        #最小日期
        if begin!=None:
            
            last=data[-1]['LISTING_DATE']
            first=data[0]['LISTING_DATE']
            try:            
                lastDate=datetime.datetime.strptime(last, "%Y-%m-%d")
                firstDate=datetime.datetime.strptime(first, "%Y-%m-%d")
                if endDate<lastDate:
                    continue
                if beginDate>firstDate:
                    break
            except:
                pass

        for d in data:
            #发行日期，决定是否写入
            LISTING_DATE=d['LISTING_DATE']
            if begin!=None:
                try:
                    thisDate=datetime.datetime.strptime(LISTING_DATE, "%Y-%m-%d")
                    if thisDate<beginDate or thisDate >endDate:
                        continue
                except:
                    continue
            
            NUM=d['NUM']
            BOND_CODE=d['BOND_CODE']
            BOND_ABBR=d['BOND_ABBR']
            BOND_FULL=d['BOND_FULL']
            PLEDGE_ABBR=d['PLEDGE_ABBR']
            PLEDGE_CODE=d['PLEDGE_CODE']
            TERM_YEAR=d['TERM_YEAR']
            INTEREST_TYPE=d['INTEREST_TYPE']
            PAY_TYPE=d['PAY_TYPE']
            ISSUE_VALUE=d['ISSUE_VALUE']

            ONLINE_START_DATE=d['ONLINE_START_DATE']
            ONLINE_END_DATE=d['ONLINE_END_DATE']
            END_DATE=d['END_DATE']

            row=[NUM,BOND_CODE,BOND_ABBR,BOND_FULL,PLEDGE_ABBR,PLEDGE_CODE,TERM_YEAR,INTEREST_TYPE,PAY_TYPE,ISSUE_VALUE,LISTING_DATE,ONLINE_START_DATE,ONLINE_END_DATE,END_DATE]
            print(row)
            csv_write.writerow(row)

def choose():
    isfull=input('是否抓取所有信息(0否1是)：')
    if isfull=='0':
        begin=input('请输入开始日期(yyyy-mm-dd):')
        end=input('请输入结束日期(yyyy-mm-dd):')
        main(None,begin,end)
    elif isfull=='1':
        #获取当前日期
        today=datetime.datetime.now().strftime('%Y-%m-%d')
        main(today)
    else:
        print('请按要求输入')
        choose()
choose()