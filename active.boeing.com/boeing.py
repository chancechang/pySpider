from bs4 import BeautifulSoup
import requests
import time
import xlsxwriter

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

def getObj(url):
    for i in range(5):
        time.sleep(2)
        try:
            req=requests.get(url,proxies=get_proxies_abuyun(), timeout=15)
            req.encoding='iso-8859-1'
            # print(req.text)
            bsObj=BeautifulSoup(req.text,'html.parser')
            table=bsObj.find_all('table',{'cellpadding':'1','cellspacing':'1'})
            if len(table)==2:
                return table
            # trlist=bsObj.find('div',class_='right').find_all('tr')
            # return bsObj
        except:
            time.sleep(3)
        if i==4:
            return None

def main():
    f1=open('active.boeing.com/boeing_up.txt','a+',encoding='utf-8',newline='')
    f_error=open('active.boeing.com/error2.txt','a+',encoding='utf-8',newline='')
    f2=open('active.boeing.com/boeing_down.txt','a+',encoding='utf-8',newline='')
    for line in open('active.boeing.com/error1.txt','r',encoding='utf-8'):
        ini=line
        line=line.split('\t')
        line[1]=line[1].strip()
        print(line[1])
        table=getObj(line[1])
        # table=bsObj.find_all('table',{'cellpadding':'1','cellspacing':'1'})
        # print(table[0])
        if table==None:
            f_error.write(ini)
            continue
        row1=line
        trlist=table[0].find_all('tr')

        for tr in trlist:
            row1.append(tr.get_text().replace('\n',''))
        f1.write(str(row1)+'\n')
        # print(row1)
        # print(table[1])
        trlist1=table[1].find_all('tr')[1:]
        for tr in trlist1:
            row2=[]
            row2.append(line[0])
            row2.append(line[1])
            # print(row2)
            tdlist=tr.find_all('td')
            # print(len(tdlist))
            for td in tdlist:
                row2.append(td.get_text().strip())                
            f2.write(str(row2)+'\n')
            # print(len(row2))
        # break
# main()

# workbook=xlsxwriter.Workbook('active.boeing.com/boeing.xlsx')
# sheet1=workbook.add_worksheet('sheet1')
# r=0
# for line in open('active.boeing.com/boeing_up.txt','r',encoding='utf-8'):
#     line=eval(line)
#     for i in range(len(line)):
#         sheet1.write(r,i,line[i])
#     r=r+1
# sheet2=workbook.add_worksheet('sheet2')
# r=0
# for line in open('active.boeing.com/boeing_down.txt','r',encoding='utf-8'):
#     line=eval(line)
#     if len(line)==11:
#         line=line[:7]+line[8:]
        
#     for i in range(len(line)):
#         sheet2.write(r,i,line[i])
#     r=r+1
# workbook.close()