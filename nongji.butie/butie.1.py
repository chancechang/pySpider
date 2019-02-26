
from bs4 import BeautifulSoup
import requests
import xlsxwriter
import re



page=226
privince='10内蒙古'
urlroot='http://222.143.21.233:2018/pub/GongShiSearch'

cook='__RequestVerificationToken=; __RequestVerificationToken_Lw__=4EDW+mpynwTkqW3DETpxdWrxn5W8nj6kMXUofKCESrXXkSYTWX4iH7MuETUbxuum0oVst5OqG1adH3bD5CcZHbYB/Wi/nKWUpPe6aKuBOPQ9QUbdZJ+YGMdsYzv4so8C9APWkGQV8G1anChDbon7Gc/mgNG6PDcIVRMAd79hLPg=; ASP.NET_SessionId=3xallifuxjx0o4d34efwznwj'
cook='__RequestVerificationToken=; CKIE_AD_ANGE='
dd='m+S6hUGtlQn2i+RhVMHrF2Am0045wGbq0cTIZLnTxHRD58cFn009D35pmOnJ8s2D2WwJs/cgQGdOX7soZYorHKQDQcEdOlCSZvmbbvHJbEVwzCbJVXC+Dw+LF6blmD84kkgr2189J4cuydeQR4vb/o0xtJFqrggQ0v0CMruTGKA='

header={
    'Cookie':cook,
}

data={
    '__RequestVerificationToken':dd,
    'p':'打（压）捆机'
}
def get_data():
    f=open(privince+'.txt','w+',encoding='utf-8')
    for i in range(1,page+1):
        print('第'+str(i)+'页')
        # url=urlroot+'?pageIndex='+str(i)
        # req=requests.post(url,data=data,headers=header)
        url='http://2018.nmnjbt2015.com/pub/gongshi?pageIndex='+str(i)+'&p=%E6%89%93%EF%BC%88%E5%8E%8B%EF%BC%89%E6%8D%86%E6%9C%BA'
        req=requests.get(url,headers=header)
        bsObj=BeautifulSoup(req.text,'html.parser')
        trlist=bsObj.find('table',{'width':'1190'}).find_all('tr')[1:]
        for tr in trlist:
            row=[]
            tdlist=tr.find_all('td')
            # print(len(tdlist))
            if len(tdlist)!=15:
                print('横向长度出现不为15的')
            for td in tdlist:
                row.append(td.get_text())
            f.write(str(row)+'\n')
        if len(trlist)<15:
            break
        # break
    # print(req.text)
    f.close()


def write_excel():
    workbook = xlsxwriter.Workbook(privince+ '农机购置补贴情况.xlsx') #创建工作簿
    sheet = workbook.add_worksheet()

    workformat = workbook.add_format({
    'bold':  True,                 #字体加粗
    })

    # rowname=['序号','县','所在乡(镇)','所在村组','购机者姓名','机具品目','生产厂家','产品名称','购买机型','购买数量(台)','经销商','单台销售价格(元)','单台补贴额(元)','总补贴额(元)','状态',]
    # for m in range(15):
    #         sheet.write(0,m,rowname[m],workformat)
    r=1
    for line in open(privince+'.txt','r',encoding='utf-8'):
        line=eval(line)
        for m in range(len(line)):
            sheet.write(r,m,line[m].replace('\r','').replace('\n','').replace('\t','').replace('\xa0','').strip())
        r=r+1
    workbook.close()

# get_data()

write_excel()