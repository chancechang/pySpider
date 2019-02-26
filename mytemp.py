from bs4 import BeautifulSoup
from urllib.error import HTTPError
import urllib.request
import json
import requests
# from selenium import webdriver
import csv
# import xlwt
import time
import util

def getHeaders(cook):
    headers = {
    "Cookie":cook,
    'Host':'m.dianping.com',
    'Upgrade-Insecure-Requests':'1',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    # "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    return headers

def getObj(url,proxyIs=False,cook=None,encode='utf-8'):
    for i in range(5):
        try:
            if cook==None:
                if proxyIs==False:
                    html=requests.get(url,timeout=15)
                else:
                    html=util.build_proxy_request(url)
            else:
                if proxyIs==False:
                    html=requests.get(url,headers=getHeaders(cook),verify=False)
                else:
                    header=getHeaders(cook)
                    html=util.build_proxy_request(url,None,getHeaders,None)
            html.encoding=encode  
            break
        except HTTPError as e:
            time.sleep(10)
            print('再次请求')
            print('HTTPError')
            return None
    try:
        bsObj = BeautifulSoup(html.text,'html.parser')
    except AttributeError as e:
        print('AttributeError')
        return None
    return bsObj
def postObj(url,data,encode='utf-8'):
    for i in range(5):
        try:
            html=requests.post(url,data=data)
            html.encoding=encode
            break
        except HTTPError as e:
            # time.sleep(3)
            print('再次请求')
            print('HTTPError')
            return None
    try:
        bsObj = BeautifulSoup(html.text,'html.parser')
    except AttributeError as e:
        print('AttributeError')
        return None
    return bsObj

def writetoCsv(filename,writelist,header=None):
    out=open(filename, 'w+',encoding='gb18030',newline = '')
    csv_write=csv.writer(out)
    if header!=None:
        csv_write.writerow(header)
    for wlist in writelist:
        csv_write.writerow(wlist)


#csv文件的读取
def csvRead(filename):   
    csv_reader = csv.reader(open(filename, encoding='gb18030'))
    for row in csv_reader:
        username=row[0]
        url=row[1]
        print(row[1])
        # crawl(username,url)
    return csv_reader



#获取json文件方法
def getJson(url,data,cook):
    #获取json
    f= urllib.request.Request(url,headers=getHeaders(cook))
    html=urllib.request.urlopen(f).read().decode('utf-8',"ignore")
    #post方法请求json数据
    r = requests.post(url, data = data)
    target=''
    try:
        target=json.loads(r.text)#["BusinessHallList"]  
    except:
        pass
    return target

# #可用来解决js渲染的重定向数据抓取不到问题
# def phangetObj(url,crawl,data=None):
#     driver =webdriver.PhantomJS(executable_path="phantomjs.exe")   
#     #使用浏览器请求页面
#     driver.get(url)
#     #加载3秒，等待所有数据加载完毕
#     time.sleep(3)
#     #通过id来定位元素，
#     #.text获取元素的文本数据
#     # dl=driver.find_elements_by_css_selector("#searchLeftOptions")
#     # dl=driver.find_element_by_id("searchLeftOptions")
#     # dl.click()
#     # pageSource=driver.page_source
#     # bsObj=BeautifulSoup(pageSource,"html.parser")
#     targetMsg=crawl(driver) 
#     driver.close()
#     return targetMsg


# #写入excel
# def writeToExcel(filename,data,sheetname='firstSheet',encode='utf-8',):
#     workbook=xlwt.Workbook(encoding=encode)
#     worksheet=workbook.add_sheet(sheetname,cell_overwrite_ok=True)#覆盖原单元格数据
#     for i in range(0,len(data)):
#         for j in range(0,len(data[0])):
#             worksheet.write(i,j,data[i][j])
#     workbook.save(filename)


#解析本地html文件
def soupHtml(filename,encode='utf-8'):
    return BeautifulSoup(open(filename,'r',encoding=encode).read(),'html.parser')

# class my_thread(Thread):
#     def run(self):
#         detailcrawl(self.href,self.detail,self.csv_write)
#     def __init__(self,href,detail,csv_write):
#         Thread.__init__(self)
#         self.href=href
#         self.detail=detail
#         self.csv_write=csv_write 

#     t=my_thread(newurl,detail,csv_write)
#     ThreadList.append(t)
#     t.start()
# for t in ThreadList:
#     t.join()

def excel_to_txt(excelname,txtfilename):
    xl = xlrd.open_workbook(excelname+'.xlsx') 
    table1 = xl.sheet_by_name(u"Sheet1")
    nr=table1.nrows
    f2= open(txtfilename+'.txt','w+',encoding='utf-8')
    for i in range(nr):
        row=table1.row_values(i)
        f2.write(str(row)+'\n')
    f2.close()
# excel_to_txt('疾病初版1','de_first')


def txt_to_excel(excelname,txtfilename):
    j=1
    workbook = xlsxwriter.Workbook(excelname+str(j)+'.xlsx') #创建工作簿
    sheet = workbook.add_worksheet()
    r=0
    for line in open(txtfilename+'.txt','r',encoding='utf-8'):
        line=eval(line)
        if r==60000:
            workbook.close()
            j=j+1
            workbook = xlsxwriter.Workbook(excelname+str(j)+'.xlsx') #创建工作簿
            sheet = workbook.add_worksheet()
            r=0
        for m in range(len(line)):
            sheet.write(r,m,line[m])
        r=r+1       
    workbook.close()