
import requests
import csv
import json
import time
import datetime



MAX_Page=500
cook='BIGipServerPool_app_chinabond_www=715265290.37151.0000; _pk_ses.1.0170=*; JSESSIONID=6DFA29606BC69B7DD491CA942FB2B940; _pk_id.1.0170=10c297c0f24dfa37.1546921738.4.1547037018.1547036258.'
headers = {
    'Cookie':cook,
    'Referer':'https://www.chinabond.com.cn/jsp/include/CB_CN/zqfhcx/queryForm.jsp',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest',
    'Host':'www.chinabond.com.cn',
    'Origin':'https://www.chinabond.com.cn'
    }
data={
    'queryType':'1',
    'zqdm':'',
    'zqjc':'',
    'bzbhhx':'',
    'ltcshx':'',
    'fuxfshx':'',
    'sTypehx':'0',
    'zqlb':'null',
    'eYear2':'0000',
    'col':'',
    'download':'',
    'url2':'',
    'logo':'',
    'bigPageNumber':'1',
    'pageNumber':'1',
    'zqfxr':'',
    
    'zczcq':'10',
    'bzbh':'01',
    'ltcs':'00',
    'fuxfs':'00',
    'fxqxq':'',
    'fxqxz':'',
    'fuxrqq':'1998-01-01',
    'fuxrqz':'2109-12-31',
    'dfrqq':'1998-01-01',
    'dfrqz':'2109-01-09',
    'pmllq':'',
    'pmllz':'',
    'syqxq':'',
    'syqxz':'',
    'sType':'0',
    'zqxz':'10',
    'zqdmOrder':'',
    'fxrqOrder':'',
    'hkrOrder':'',
    'qxrOrder':'',
    'dqrOrder':'',
    'ssltrOrder':'',
    'zqqxOrder':'',
    'fxfsOrder':'',
    'xOrder':'',
    'number':'1',
}

def main(data,today,begin=None,end=None):
    if begin==None:
        end=today
        begin=today[:2]+str(int(today[2:4])-1)+today[4:]
    else:
        try:
            beginDate=datetime.datetime.strptime(begin, "%Y-%m-%d")    
            endDate=datetime.datetime.strptime(end, "%Y-%m-%d")    
        except:
            print('日期不合法，请重新输入')
            return choose()
        if beginDate>endDate:
            print('起止日期不合规范，请重新输入')
            return choose()
    date=begin+'_'+end
    data['fxrqq']=begin
    data['fxrqz']=end
    f1=open(date+'债券信息_资产支持证券.csv','w+',encoding='gb18030',newline='')
    csv_write=csv.writer(f1)
    rowname=['序号','债券简称',	'债券代码',	'发行人简称',	'ISIN码'	,'债券全称'	,'发行日期'	,'计划发行量（亿元）',	'发行开始日',	'发行截止日'	,'实际发行量（亿元）','付息方式','选择权类别','票面利率（%）',	'债券期限',	'起息日'	,'到期日',	'债券信用评级','主体信用评级','付息频率（月）',	'基本利差（%）','当期基础利率（%）','首次划款日','上市流通日'	,'发行手续费率（%）','兑付手续费率（%）',	'发行价格（元）'	,'参考收益率（%）'	,'下一次赎回日'	,'债券评级机构'	,'主体评级机构'	,'浮动利率基准','剩余本金值',	'备注']
    csv_write.writerow(rowname)
    urlroot='https://www.chinabond.com.cn/zqfhcxServlet.do'
    bsObj=None
    for i in range(5):
        try:
            bsObj=requests.post(urlroot,data=data,headers=headers,timeout=15)           
            break
        except:
            pass
    if bsObj==None:
        print('error')
        return
    data=json.loads(bsObj.text)['vVector']
    le=len(data)
    for i in range(1,le):
        d=data[i]
        row=[]
        row.append(str(i))
        row.append(d[30])
        row.append(d[1])
        row.append(d[28])
        row.append(d[22])
        row.append(d[0])
        row.append(d[2])
        row.append(d[3])
        row=row+d[31:33]
        row.append(d[4])
        row.append(d[5])#付息方式
        row.append(d[19])#选择权类别

        row.append(d[7])#票面利率
        row.append(d[21])#债券期限
        row=row+d[11:13]
        row.append(d[23])#债券信用评级
        row.append(d[25])#主体信用评级
        row.append(d[6])#付息频率（月）
        row=row+d[8:11]
        row.append(d[13])#付息频率（月）
        row=row+d[14:19]
        row.append(d[24])#债券评级机构
        row.append(d[26])#债券评级机构
        row.append(d[27])#债券评级机构
        row.append(d[29])#债券评级机构
        row.append(d[33])#债券评级机构
        print(row)
        csv_write.writerow(row)
    

def choose(data):
    isfull=input('是否抓取所有信息(0否1是)：')
    if isfull=='0':
        begin=input('请输入开始日期(yyyy-mm-dd):')
        end=input('请输入结束日期(yyyy-mm-dd):')
        main(data,None,begin,end)
    elif isfull=='1':
        #获取当前日期
        today=datetime.datetime.now().strftime('%Y-%m-%d')
        main(data,today)
    else:
        print('请按要求输入')
        choose()
choose(data)