
from bs4 import BeautifulSoup
import requests
import xlsxwriter







# f=open('link.txt','w+',encoding='utf-8')

# for i in range(1,1422):
#     url='http://jobs.kq88.com/index.php?s=/Home/Searchlist/index//p/'+str(i)
#     req=requests.get(url)
#     bsObj=BeautifulSoup(req.text,'html.parser')
#     ul=bsObj.find('ul',{'id':'ltd_list_con'})
#     lilist=ul.find_all('li',class_='list_job')
#     print(len(lilist))
#     for li in lilist:
#         a=li.find('a',class_='list_dl')
#         href=a.attrs['href']
#         name=li.find('a',class_='item-ent-name').get_text().replace('Vip','').strip()
#         # print(li)
#         shi=li.find('span',class_='job-loc').get_text()
       
            
#         row=[href,name,shi]
#         f.write(str(row)+'\n')
# f.close()

def get_detail():

    f1=open('detail.txt','w+',encoding='utf-8')
    f2=open('link_error.txt','w+',encoding='utf-8')

    root='http://jobs.kq88.com'
    i=0
    for line in open('link.txt','r',encoding='utf-8'):
        print(i)
        i=i+1
        line=eval(line)
        url=root+line[0]
        # url='http://jobs.kq88.com/37813.html'
        try:
            req=requests.get(url,timeout=15)
        except:
            f2.write(str(line)+'\n')
            continue

        bsObj=BeautifulSoup(req.text,'html.parser')
        ul=bsObj.find('div',class_='blk_2013 apply_hosp')
        line.append(str(ul))
        f1.write(str(line)+'\n')
        # break
    f1.close()
    f2.close()

def write_excel():
    
    workbook = xlsxwriter.Workbook('kq88.xlsx') #创建工作簿
    sheet = workbook.add_worksheet()
    r=0

    for line in open('detail.txt','r',encoding='utf-8'):
        line=eval(line)
        # print(line)
        bsObj=BeautifulSoup(line[3],'html.parser')
        phone=bsObj.find('strong').get_text()
        other=bsObj.find_all('p')[-1].get_text().split(phone)
        row=line[:3]+[phone]+other
        for i in range(len(row)):
            sheet.write(r,i,row[i].replace('\r','').replace('\n','').replace('\t','').replace('\xa0','').strip())
        r=r+1
        # print(r)
        # print(row)
        # break
    workbook.close()
    

write_excel()
        
