
import requests
from bs4 import BeautifulSoup
import base64
import json
import xlrd
import xlsxwriter
# cook='_gscu_1718069323=50562795wcg7ou84; _gscbrs_1718069323=1; JSESSIONID=4dcc9e8421d9a5f10a127fdf62bc'
# cook='_gscu_1718069323=50562795wcg7ou84; _gscbrs_1718069323=1; JSESSIONID=4e222f257e931292abb06d6f14d5'
# cook='_gscu_1718069323=50562795wcg7ou84; _gscbrs_1718069323=1; JSESSIONID=4eb7ddf2891f8193038614f7415c'
# cook='_gscu_1718069323=50562795wcg7ou84; _gscbrs_1718069323=1; JSESSIONID=63936ba5d3c3d12e5544054d5ce2'
# cook='_gscu_1718069323=50562795wcg7ou84; _gscbrs_1718069323=1; JSESSIONID=8b20f2179d8b1f3e5c3523ee6660'
cook='_gscu_1718069323=50562795wcg7ou84; _gscbrs_1718069323=1; JSESSIONID=8c8adbc43790ff7a00996630d2f9'
header={
    'Cookie': cook,
    'Host': 'cpquery.sipo.gov.cn',
    'Referer': 'http://cpquery.sipo.gov.cn/txnPantentInfoList.do?inner-flag:open-type=window&inner-flag:flowno=1550556201521',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}



def get_code(header):
    url='http://cpquery.sipo.gov.cn/freeze.main?txn-code=createImgServlet&freshStept=1&now=Tue%20Feb%2019%202019%2015:03:10%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)'
    i=0
    r=requests.get(url,headers=header)
    r.raise_for_status()
    path='./img/'+str(i)+'.jpeg'
    with open(path, "wb") as f:  # 开始写文件，wb代表写二进制文件
        f.write(r.content)
        print("爬取完成")

    with open("./img/0.jpeg", 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()


    accessToken='24.50270a9f54d3665d7f614cc30fdb0688.2592000.1553142168.282335-15585652'
    # url_ocr='https://ai.baidu.com/aidemo?'+'access_token='+accessToken
    url_ocr='https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?'+'access_token='+accessToken
    header={
        'Content-Type':	'application/x-www-form-urlencoded'
    }
    data={
        # 'type': 'commontext',
        'image': s
    }
    code=requests.post(url_ocr,data=data,headers=header,timeout=10)

    try:
        words=json.loads(code.text)['words_result'][0]['words'].replace(':','')
        print('计算公式:'+words)
        if '+' in words:
            code=int(words[0])+int(words[2])
        elif '-' in words:
            code=int(words[0])-int(words[2])
        else:
            code=input('请输入：')
    except:
        code=input('请输入：')
    return code


def excel_to_txt():
    xl = xlrd.open_workbook('hangkong2019.xlsx') 
    table1 = xl.sheet_by_name(u"实际控制权")
    nr=table1.nrows
    f2= open('hangkong.txt','w+',encoding='utf-8')
    for i in range(nr):
        row=table1.row_values(i)
        f2.write(str(row)+'\n')
    f2.close()

def main(header):
    f=open('detailzl.txt','a+',encoding='utf-8')
    f_error=open('error1.txt','a+',encoding='utf-8')
    for line in open('error.txt','r',encoding='utf-8'):
        line=eval(line)
        # code=input('请输入：')
        code=get_code(header)
        company=line[2]
        print(company)
        # company='山东联诚精密制造股份有限公司'
        url='http://cpquery.sipo.gov.cn/txnQueryOrdinaryPatents.do?select-key:shenqingh=&select-key:zhuanlimc=&select-key:shenqingrxm='+str(company)+'&select-key:zhuanlilx=&select-key:shenqingr_from=&select-key:shenqingr_to=&verycode='+str(code)+'&inner-flag:open-type=window&inner-flag:flowno=1550556210285&attribute-node:record_page-row=8000&'
        # url='http://cpquery.sipo.gov.cn//txnQueryOrdinaryPatents.do?select-key%3Ashenqingh=&select-key%3Azhuanlimc=&select-key%3Ashenqingrxm='+str(company)+'&select-key%3Azhuanlilx=&select-key%3Ashenqingr_from=&select-key%3Ashenqingr_to=&very-code=&captchaNo=&fanyeflag=1&verycode=fanye&attribute-node:record_start-row=1&attribute-node:record_page-row=100&'
            # 'http://cpquery.sipo.gov.cn//txnQueryOrdinaryPatents.do?select-key%3Ashenqingh=&select-key%3Azhuanlimc=&select-key%3Ashenqingrxm=%E6%B1%9F%E8%A5%BF%E9%87%91%E5%8A%9B%E6%B0%B8%E7%A3%81%E7%A7%91%E6%8A%80%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&select-key%3Azhuanlilx=&select-key%3Ashenqingr_from=&select-key%3Ashenqingr_to=&very-code=&captchaNo=&fanyeflag=1&verycode=fanye&attribute-node:record_start-row=21&attribute-node:record_page-row=10&'
        req=requests.get(url,headers=header)
        bsObj=BeautifulSoup(req.text,'html.parser')
        print(req)
        divlist=bsObj.find_all('div',class_='content_listx')
        le=len(divlist)
        print(le)
        # break

        if le==0 or  le==8000:
            f_error.write(str(line[:3])+'\n')
            continue
        for j in range(le):
            row=line[:3]+[str(divlist[j]).replace('\n','')]
            f.write(str(row)+'\n')
        break
        
# main(header)

def txt_to_excel():
    j=1
    workbook = xlsxwriter.Workbook('2019航空'+str(j)+'.xlsx') #创建工作簿
    sheet = workbook.add_worksheet()
    r=0
    for line in open('hangkong_final.txt','r',encoding='utf-8'):
        line=eval(line)
        if r==60000:
            workbook.close()
            j=j+1
            workbook = xlsxwriter.Workbook('2019航空'+str(j)+'.xlsx') #创建工作簿
            sheet = workbook.add_worksheet()
            r=0
        for m in range(len(line)):
            sheet.write(r,m,line[m])
        r=r+1       
    workbook.close()
txt_to_excel()

def chuli():
    f=open('detail_final.txt','w+',encoding='utf-8')
    for line in open('detailzl.txt','r',encoding='utf-8'):
        line=eval(line)
        bsObj=BeautifulSoup(line[3],'html.parser')
        tdlist=bsObj.find('tr').find_all('td')
        le=len(tdlist)
        if le!=6:
            break
        row=line[:3]
        for i in range(5):
            row.append(tdlist[i].get_text())
        f.write(str(row)+'\n')
    f.close()


def hangkong():
    f=open('hangkong_final.txt','w+',encoding='utf-8')
    for line in open('hangkong.txt','r+',encoding='utf-8'):
        line=eval(line)
        le=len(line)
        # print(le)
        for i in range(4,le,2):
            # print(i)
            # if line[i]=='':
            #     print('查到最后')
            #     print(line[1],line[i-2])
            #     break
            # print(line[i],line[1])
            if line[i]==line[1]:
                floor=int(i/2)-1
                if '宝鸡市易' in line[1]:

                    print(line[2:4])
                row=[line[1],line[0]]+line[2:4]+[str(floor)+'级子公司']+[line[i-2]]
                # print(row)
                f.write(str(row)+'\n')
                break

        # break
# hangkong()
excel_to_txt()
