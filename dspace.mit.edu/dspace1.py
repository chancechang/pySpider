from bs4 import BeautifulSoup
import requests
import xlsxwriter
import json

def get_link():
    '''
    获取文章链接
    '''
    f=open('article_linka.txt','a+',encoding='utf-8')
    for i in range(1,150):
        print('第'+str(i)+'页')
        url='https://dspace.mit.edu/handle/1721.1/5458/browse?order=DESC&rpp=20&sort_by=2&etal=-1&offset='+str(i*20)+'&type=dateissued'
        # 获取网页内容
        req=requests.get(url)
        #网页解析
        bsObj=BeautifulSoup(req.text,'html.parser')
        ul=bsObj.find('ul',class_='ds-artifact-list')
        lilist=ul.find_all('li',class_='ds-artifact-item')
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
    '''
    获取详细信息,写入txt
    '''
    f=open('article.txt','a+',encoding='utf-8')
    m=1
    for line in open('article_linka.1.txt','r',encoding='utf-8'):
        line=eval(line)
        url='https://dspace.mit.edu'+line[0]
        print('正在爬取第'+str(m)+'个')
        print(url)  
        req=requests.get(url)
        bsObj=BeautifulSoup(req.text,'html.parser')  

        #摘要
        try:
            abstract=bsObj.find('div',class_='simple-item-view-description').get_text().replace('Abstract:','')
        except:
            abstract=''
        #关键字
        divlist=bsObj.find_all('div',class_='simple-item-view-other')
        for d in divlist:
            if 'Keywords:' in d.get_text():
                keyword=d.get_text().replace('Keywords:','')
                break
        #取到作者并根据；分开成list
        author=bsObj.find('div',class_='simple-item-view-authors').get_text().replace('Author:','').split(';')
        row=[line[1],abstract,keyword]+author
        f.write(str(row)+'\n')
        m=m+1        
        
        # print(row)
        # break
    f.close()


def write_to_excel():
    '''
    从txt写入excel
    '''
    #新建excel 文件名为article
    workbook = xlsxwriter.Workbook('author_country1.xlsx') #创建工作簿
    sheet = workbook.add_worksheet() #创建sheet
    r=0 #sheet的行
    #excel标题名称
    # rowname=['文章名','摘要','关键词','作者1','作者2','作者3','作者4','作者5','作者6',]
    rowname=['姓名','country']
    for m in range(len(rowname)):
        sheet.write(r,m,rowname[m])
    r=r+1
    for line in open('author_country1.txt','r',encoding='utf-8'):
        line=eval(line)
        #写到excel单元格
        for m in range(len(line)):
            sheet.write(r,m,line[m].replace('\n',''))
        r=r+1 #行数加一
    workbook.close()   #关闭并保存excel 
    


def get_country():
    header={
        # 'X-API-KEY':'9350c16ec66c06b218e8adb55634d737',
        'X-API-KEY':'4436d93940f8d7c42b9acfb9ab144fa7',
        'Cookie':'_ga=GA1.2.640708097.1548917769; _gid=GA1.2.1389663980.1548917769',
        'accept': 'application/json'
    }
    r=1
    f=open('author_country1.txt','a+',encoding='utf-8')
    for line in open('author_country.txt','r',encoding='utf-8'):
        line=eval(line)
        name=line[0]
        if line[1]=='US':
            url='https://v2.namsor.com/NamSorAPIv2/api2/json/country/'+name
            req=requests.get(url,headers=header)
            print(req.text)
            js=json.loads(req.text)
            row=[name,js['country'],js['region']]
            print(r)       
            print(row)
            f.write(str(row)+'\n')
        else:
            print(r)
            f.write(str(line)+'\n')
        r=r+1
    f.close()

# get_country()  

# get_link()
# get_detail()
# write_to_excel()

