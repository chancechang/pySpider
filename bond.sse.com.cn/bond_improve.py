
import requests
import csv
import json
import time

#日期，必须小于等于当前日期，格式为XXXX-XX-XX
date='2018-10-22'
MAX_Page=100



headers = {
    'Referer':'http://bond.sse.com.cn/data/statistics/survey/single/',
    'Host':'query.sse.com.cn'
    }
      
def main():
    urlroot='http://query.sse.com.cn/commonQuery.do?isPagination=true&sqlId=COMMON_SSEBOND_SCSJ_SCTJ_CJSJ_GQCJTJ_L&pageHelp.pageSize=20&START_DATE='+date+'&END_DATE='+date
    # urlroot='http://query.sse.com.cn/commonQuery.do?isPagination=true&sqlId=COMMON_SSEBOND_SCSJ_SCTJ_CJSJ_GQCJTJ_CX_L&pageHelp.pageSize=20&BOND_CODE=&START_DATE=2018-10-18&END_DATE=2018-10-18&_=1542528393369'
    f1=open(date+'个券成交统计.csv','w+',encoding='gb18030',newline='')
    csv_write=csv.writer(f1)
    csv_write.writerow(['代码','名称','成交笔数','成交金额(万元)','加权平均价格'])
    for i in range(1,MAX_Page,5):
        url=urlroot+'&pageHelp.pageNo='+str(i+1)+'&pageHelp.beginPage='+str(i)+'&pageHelp.endPage='+str(i+4)
        for i in range(5):
            try:
                bsObj=requests.get(url,headers=headers)
                break
            except:
                pass
        if bsObj==None:
            print('error')
            break
        data=json.loads(bsObj.text)['pageHelp']['data']
        if len(data)==0:
            break
        for d in data:
            BOND_CODE=d['BOND_CODE']
            BOND_ABBR=d['BOND_ABBR']
            VOLUME=d['VOLUME']
            AMOUNT=d['AMOUNT']
            AVG_PRICE=d['AVG_PRICE']
            row=[BOND_CODE,BOND_ABBR,VOLUME,AMOUNT,AVG_PRICE]
            print(row)
            csv_write.writerow(row)
main()