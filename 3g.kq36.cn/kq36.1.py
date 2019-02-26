
from bs4 import BeautifulSoup
import requests
import xlsxwriter
import re




def get_link():
    name='全国公立医院'
    f=open(name+'link1.txt','a+',encoding='utf-8')
    f1=open(name+'error1.txt','a+',encoding='utf-8')
    for i in open(name+'error.txt','r',encoding='utf-8'):
        print('第'+str(i)+'页')
        url='https://3g.kq36.cn/2000/?pageindex='+str(i)
        req=requests.get(url)
        bsObj=BeautifulSoup(req.text,'html.parser')
        ul=bsObj.find('table',{'id':'thelist'})
        try:
            lilist=ul.find_all('tr')
        except:
            f1.write(str(i))
            continue
        print(len(lilist))
        for tr in lilist:
            a=tr.find('a')
            href=a.attrs['href']
            if 'javascript' in href:
                # print(a.attrs['onclick'])
                href=re.search(r"else{\$\(this\).attr\(\'href\',\'(.+?)\'\)}",a.attrs['onclick']).group(1)
            name=tr.find('li',class_='title').get_text().strip()
            address=tr.find('li',class_='titlec').get_text().strip()
            # print(li)
            row=[href,name,address]
            f.write(str(row)+'\n')
        if len(lilist)<10:
            break
    f.close()
    f1.close()

# get_link()

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
    

def get_detail():
    name='全国公立医院'
    f1=open(name+'detail.txt','a+',encoding='utf-8')
    f2=open(name+'link_error3.txt','a+',encoding='utf-8')

    # root='http://jobs.kq88.com'
    # 'https://www.kq159.com/yayale508/?comid=3&comname=%E5%85%A8%E5%9B%BD%E7%89%99%E7%A7%91&tmp=1548062662000'
    # 'https://3g.kq36.com/jobs/2187733'
    i=0
    for line in open(name+'link_error2.txt','r',encoding='utf-8'):
        print(i)
        line=eval(line)
        url=line[0]
        if 'www.kq159.com' in url:
            # om/yy828083/?comid=3&com
            id=re.search(r'ww.kq159.com/(.+?)/\?comid=',url).group(1)
            print(id)
            url='https://www.kq159.com/'+id+'/contact.html?'
        print(url)
        
        for m in range(5):
            try:
                if '3g.kq36.com' in url:
                    req=requests.get(url,timeout=15,proxies=get_proxies_abuyun())
                    req.encoding='gb2312'
                    break
                else:
                    req=requests.get(url,timeout=15)
                    req.encoding='utf-8'
                    break
            except:
                pass
        if m==4:
            f2.write(str(line)+'\n')
            continue

        bsObj=BeautifulSoup(req.text,'lxml')

        if '3g.kq36.com' in url:
            # row=g_kq36(url,f2)
            # print(bsObj)
            # break
            if '3g.kq36.com/jobs' in url:
                div=bsObj.find('div',class_='r4')
                line.append(str(div))
            else:
                div=bsObj.find('div',class_='r1')
                line.append(str(div))
                
            
            
        elif 'www.kq159.com' in url:           
            div=bsObj.find('ul',class_='c_infos')      
            line.append(str(div))  
            # print(div)
            # break 
        else:
            f2.write(str(line)+'\n')
            continue
        # print(line)
        f1.write(str(line)+'\n')
        # break
        i=i+1
        
        # if i==10:
        #     break
    f1.close()
    f2.close()


# get_detail()



def write_excel():
    name='全国牙科'
    workbook = xlsxwriter.Workbook(name+'.xlsx') #创建工作簿
    sheet = workbook.add_worksheet()
    r=0

    for line in open('qgykdetail.txt','r',encoding='utf-8'):
        line=eval(line)
        # print(line)
        url=line[0]
        wx=''
        phone=''
        t_phone=''
        mail=''
        address=''
        web_url=''
        p_name=''
        bsObj=BeautifulSoup(line[3],'lxml')
        if '3g.kq36.com' in url:
            if 'govzp' in url:
                div=bsObj.find_all('div')
                for d in div:
                    if '联系' in d.get_text():
                        p_name=d.get_text().replace('联系','')
                        continue
                    if '电话' in d.get_text():
                        alist=d.find_all('a')
                        for a in alist:
                            phone=phone+a.attrs['href']+'_'
                        continue
                    if '邮件' in d.get_text():
                        mail=d.get_text().replace('邮件','')
                        continue
                    if '地址' in d.get_text():
                        address=d.get_text().replace('地址','')
                        continue
                    if '官网' in d.get_text():
                        web_url=d.get_text().replace('官网','')
                        continue

            else:
                div=bsObj.find_all('ul')
                for ul in div:
                    if '电话' in ul.get_text():
                        t_phone=ul.find('li',class_='c2').get_text()
                        continue
                    if '联系' in ul.get_text():
                        p_name=ul.find('li',class_='c2').get_text()
                        continue
                        
                    if '手机' in ul.get_text():
                        try:
                            ali=ul.find('li',class_='c2').find_all('a')
                            for a in ali:
                                phone=phone+a.attrs['href']+'_'
                            # phone=ul.find('li',class_='c2').find('a').attrs['href']
                        except:
                            phone=ul.find('li',class_='c2').get_text()
                        continue
                        
                    if '微信' in ul.get_text():
                        wx=ul.find('li',class_='c2').get_text()
                        continue
                        
                    if '邮箱' in ul.get_text():
                        try:
                            mail=ul.find('li',class_='c2').find('a').attrs['href']
                        except:
                            mail=ul.find('li',class_='c2').get_text()
                        continue
                        
                    if '地址' in ul.get_text():
                        address=ul.find('li',class_='c2').get_text()
                        continue
                                
            
        elif 'www.kq159.com' in url: 
            try:          
                p_name=bsObj.find('li',class_='c_p1').get_text()
            except:
                p_name=''
            try:
                
                ali=bsObj.find('li',class_='c_p2').find_all('a')
                for a in ali:
                    hr=a.attrs['href']
                    if 'javasc' in hr:
                        hr=a.get_text()
                    phone=phone+hr+'_'
            except:
                phone=''
            try:
                mail=bsObj.find('li',class_='c_p4').get_text().split('?')[0]
            except:
                mail=''
            try:
                wx=bsObj.find('li',class_='c_p7').get_text()
            except:
                wx=''
            try:
                web_url=bsObj.find('li',class_='c_p8').get_text()
            except:
                web_url=''
            try:
                address=bsObj.find('li',class_='c_p5').get_text()
            except:
                address=''
        else:
            pass
        if phone=='' and mail=='' and wx==''and t_phone=='':
            continue
        address=address.split('地图')[0]
        if len(phone)>255:
            phone=''
        row=line[:2]+[p_name,t_phone,phone,mail,wx,web_url,address] 
        

        for i in range(len(row)):
            # if len(row[i])>255:
            #     print(row)
            #     print(i)
            #     row[i]=''
            sheet.write(r,i,row[i].replace('\r','').replace('\n','').replace('\t','').replace('\xa0','').strip())
        r=r+1
        # print(r)
        # print(row)
        # break
    workbook.close()
    

write_excel()
        

# def get_detail():

#     f1=open(name+'detail.txt','a+',encoding='utf-8')
#     f2=open(name+'link_error.txt','a+',encoding='utf-8')

#     # root='http://jobs.kq88.com'
#     # 'https://www.kq159.com/yayale508/?comid=3&comname=%E5%85%A8%E5%9B%BD%E7%89%99%E7%A7%91&tmp=1548062662000'
#     # 'https://3g.kq36.com/jobs/2187733'
#     i=0
#     for line in open(name+'link.txt','r',encoding='utf-8'):
#         print(i)
#         i=i+1
#         line=eval(line)
#         url=line[0]
#         if 'www.kq159.com' in url:
#             # om/yy828083/?comid=3&com
#             id=re.search(r'ww.kq159.com/(.+?)/\?comid=',url).group(1)
#             print(id)
#             url='https://www.kq159.com/'+id+'/contact.html?'
#         print(url)
        
#         try:
#             if '3g.kq36.com' in url:
                
#                 req=requests.get(url,timeout=15,proxies=get_proxies_abuyun())
#                 req.encoding='gb2312'
#             else:
#                 req=requests.get(url,timeout=15)
#                 req.encoding='utf-8'
                
#         except:
#             f2.write(str(line)+'\n')
#             continue

#         bsObj=BeautifulSoup(req.text,'lxml')
#         ul=bsObj.find('ul',class_='c_infos')
#         try:
#             mainUrl=ul.find('li',class_='c_p1').get_text()
#             phone=ul.find('li',class_='c_p2').find('a').attrs['href']
#             address=ul.find('li',class_='c_p5').get_text()        
#         except:
#             f2.write(str(line)+'\n')
#             continue
#         # print(line)
#         line=line+[mainUrl,phone,address]
#         f1.write(str(line)+'\n')
#         # break
#         # if i==10:
#         #     break
#     f1.close()
#     f2.close()


# # get_detail()


# def write_excel():
    
#     workbook = xlsxwriter.Workbook(name+'.xlsx') #创建工作簿
#     sheet = workbook.add_worksheet()
#     r=0

#     for line in open(name+'detail.txt','r',encoding='utf-8'):
#         row=eval(line)
#         # print(line)
        
#         for i in range(len(row)):
#             sheet.write(r,i,row[i].replace('\r','').replace('\n','').replace('\t','').replace('\xa0','').strip())
#         r=r+1
#         # print(r)
#         # print(row)
#         # break
#     workbook.close()
    

# write_excel()
        
