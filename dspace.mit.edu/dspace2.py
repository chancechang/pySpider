from bs4 import BeautifulSoup
import requests
import re
import xlsxwriter



def get_link():

    f=open('author_link.txt','a+',encoding='utf-8')
    for i in range(0,150):
        print('第'+str(i)+'页')
        url='https://dspace.mit.edu/handle/1721.1/29807/browse?order=ASC&rpp=20&sort_by=-1&etal=-1&offset='+str(i*20)+'&type=author'
        req=requests.get(url)
        bsObj=BeautifulSoup(req.text,'html.parser')
        lilist=bsObj.find_all('tr',class_='ds-table-row')
        for li in lilist:
            a=li.find('a')
            title=a.get_text()
            link=a.attrs['href']
            row=[link,title]
            f.write(str(row)+'\n')
        print('该页数量为'+str(len(lilist)))
        if len(lilist)<20:
            break
        # break
    f.close()


def get_detail():
    f=open('author.txt','a+',encoding='utf-8')
    m=0
    for line in open('author_link.txt','r',encoding='utf-8'):
        line=eval(line)
        url='https://dspace.mit.edu/handle/1721.1/29807/'+line[0]
        m=m+1
        print(m)
        print(url)  
        req=requests.get(url)
        bsObj=BeautifulSoup(req.text,'html.parser')  
        row=[url,line[1]]
        #文章
        divlist=bsObj.find_all('li',class_='ds-artifact-item')
        print(len(divlist))
        if len(divlist)==10 or len(divlist)==20 or len(divlist)==15:
            print(row)
            break
        for d in divlist:
            row.append(d.find('a').get_text())
        f.write(str(row)+'\n')
        row=[]
    f.close()


def write_to_excel():
    workbook = xlsxwriter.Workbook('article_部分.xlsx') #创建工作簿
    sheet = workbook.add_worksheet()
    r=0
    # rowname=['作者','文章1','文章2','文章3','文章4','文章5','文章6','文章7']
    rowname=['文章名','摘要','关键词','作者1','作者2','作者3','作者4','作者5','作者6',]

    for m in range(len(rowname)):
        sheet.write(r,m,rowname[m])
    r=r+1
    for line in open('test.txt','r',encoding='utf-8'):
        line=eval(line)
        for m in range(len(line)):
            sheet.write(r,m,line[m].replace('\n',''))
        r=r+1
    workbook.close()  
write_to_excel()





 
