from bs4 import BeautifulSoup
import requests
import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
import re
import xlsxwriter
import os



def phangetObj(url):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
    )
    dcap["phantomjs.page.settings.cookie"] = (
    header['Cookie']
    )
    driver =webdriver.PhantomJS(executable_path="phantomjs.exe",desired_capabilities=dcap)   
    #使用浏览器请求页面
    driver.get(url)
    #加载3秒，等待所有数据加载完毕
    time.sleep(3)
    #通过id来定位元素，
    #.text获取元素的文本数据
    # dl=driver.find_elements_by_css_selector("#searchLeftOptions")
    # dl=driver.find_element_by_id("searchLeftOptions")
    # dl.click()
    pageSource=driver.page_source

    return pageSource
def sendmsg(msg,from_addr,password,to_addr):
    # 输入SMTP服务器地址:
    smtp_server = 'smtp.qq.com'  #163邮箱为'smtp.163.com'
    server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()    

def test_email():
    from_addr = '85386227@qq.com'
    # from_addr = '1509662199@qq.com'

    password = 'qzlqxznqbzbcbhbj'
    # password = 'chang222701'
    to_addr = '1509662199@qq.com'
    msg = MIMEText('this is a test', 'plain', 'utf-8')
    sendmsg(msg,from_addr,password,to_addr)

cook='_med=dw:1366&dh:768&pw:1366&ph:768&ist:0; cna=h9/yEVZzcBsCAXrNB8OEFnAP; hng=CN%7Czh-CN%7CCNY%7C156; t=8464a4877acc365c142612d5c3535d73; tracknick=chang19961122; lid=chang19961122; _tb_token_=eb5635e78e1b7; cookie2=107016ae7cf97f2274ad063d975761ff; uc1=cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&cookie21=W5iHLLyFfXVRCJf5lG0u7A%3D%3D&cookie15=W5iHLLyFOGW7aA%3D%3D&existShop=true&pas=0&cookie14=UoTYMhq%2FKhYQPA%3D%3D&tag=8&lng=zh_CN; uc3=vt3=F8dByRzKEOtARWtl%2Bgw%3D&id2=UUphyI2MZooAgg%3D%3D&nk2=AHLWi98GGcUQYFQdBA%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; _l_g_=Ug%3D%3D; ck1=""; unb=2202500475; lgc=chang19961122; cookie1=ACk3%2Bif10PWqoXfHbTWBPMBOKPczrDoVRwUORIU6cts%3D; login=true; cookie17=UUphyI2MZooAgg%3D%3D; _nk_=chang19961122; uss=""; csg=ad4359a1; skt=b92b00e5d2e5368d; enc=vMQz56qGe2HJazNG1xFfetmejeDOMcarLVyCtMWS7eBnBoW5YRQrhWB2Hscg%2BV4wl%2FGrmKaEdu45R2AYpKY3tQ%3D%3D; res=scroll%3A1349*5342-client%3A1349*662-offset%3A1349*5342-screen%3A1366*768; pnm_cku822=098%23E1hvxQvUvbpvUvCkvvvvvjiPR2Fp1jiUPscygjEUPmPZ1jimnLzOtj38n2cWgjimiQhvCvvvpZptvpvhvvCvpvGCvvpvvPMMvphvC9mvphvvvbyCvm9vvhCvvvvvvvvvBBWvvvHbvvCHhQvv9pvvvhZLvvvCfvvvBBWvvvH%2BkphvC9hvpyPO68yCvv9vvhhe7DpdjvyCvhACUnf7jweARdItb9TxfX94dixdBTc6eCe4VcDx0f06W3vOJ1kHsfUpeEDTmEcBKFyzhmx%2Ftj7J%2Bu04jLPnQL46R3Bkp8oQ%2Bu0OVC69; cq=ccp%3D0; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=205411; whl=-1%260%260%260; isg=BDMz7zCLa9epXCAMMAheICE-wjeHrSl-hovZyeXQz9KK5FOGbTt0eN1-mlSvxB8i; x=__ll%3D-1%26_ato%3D0'
header={
    'Cookie':cook,
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    # 'X-DevTools-Emulate-Network-Conditions-Client-Id':'(6E111686F4C1612F892FF0F1862152BE)'
}
def get_link():
    f=open('ydjd_link.txt','w+',encoding='utf-8',newline='')
    for i in range(0,8):
        url='https://list.tmall.com/search_shopitem.htm?s='+str(i*60)+'&oq=%D2%C1%B6%D9%BC%CD%B5%C2%C6%EC%BD%A2%B5%EA&style=sg&sort=s&user_id=400677264&stype=search'
        req=requests.get(url,headers=header)
        bsObj=BeautifulSoup(req.text,'html.parser')
        divList=bsObj.find('div',{'id':'J_ItemList'}).find_all('div',class_='product')
        print(len(divList))
        for d in divList:
            sr=d.find('a',class_='productImg').find('img').attrs['data-ks-lazyload']
            a=d.find('p',class_='productTitle').find('a')
            a_p=d.find('p',class_='productPrice').get_text().replace('\n','')
            title=a.attrs['title']
            href=a.attrs['href']
            row=[href,sr,title,a_p]
            print(row)
            f.write(str(row)+'\n')
        # break
    f.close()

def get_detail(url):    
    # req=requests.get(url,headers=header)
    req=phangetObj(url)
    bsObj=BeautifulSoup(req,'html.parser')
    # print(bsObj)
    s_list=bsObj.find_all('script')
    detail_json=''
    price_json=''
    for s in s_list:
        t=s.get_text()
        if '_DATA_Detail' in t:
            detail_json=t.split('_DATA_Detail')[1].replace(';','').replace('=','')
            continue
        if '_DATA_Mdskip' in t:
            price_json=t.split('_DATA_Mdskip')[1].replace(';','').replace('=','')           
    if detail_json =='' or price_json=='':
        print('error  '+url)    
    # print(detail_json)
    #产品信息
    detail=json.loads(detail_json )['props']['groupProps'][0]['基本信息']
    price=json.loads(price_json)['price']
    return [detail,price]
def get_detailList():
    f=open('detail_list.txt','a+',encoding='utf-8',newline='')
    for line in open('ydjd_link.txt','r',encoding='utf-8'):
        line=eval(line)
        url='https:'+line[0]
        # url='https://detail.tmall.com/item.htm?id=557603631033&areaId=420100&is_b=1&cat_id=2&rn=60fb488bf3da9c64b20d1f67712f2213'
        print(url)
        row=line+get_detail(url)
        print(row)
        f.write(str(row)+'\n')
        # break   
    f.close()

def main():
    workbook = xlsxwriter.Workbook('伊顿纪德.xlsx')     #创建工作簿
    sheet = workbook.add_worksheet()    
    rowname=['商品链接','图片','品名','原价','现价','材质成分','上市','适用季节','适用性别','参考身高']
    r=0
    for n in range(len(rowname)):
        sheet.write(r,n,rowname[n])
    r=1
    for line in open('detail_list.txt','r',encoding='utf-8'):
        line=eval(line)
        row=['' for t in range(len(rowname)+1)]
        row[0]='https:'+line[0]
        row[1]='https:'+line[1]
        row[2]=line[2]
        if '裤' in line[2]:
            row[-1]='裤子'
        #详细信息
        for det in line[4]:
            for i in range(len(rowname)):
                if rowname[i] in str(det):
                    for key,value in det.items():
                        row[i]=value
                        break
                if '面料' in str(det):
                    for key,value in det.items():
                        row[5]=value
        #价格
        # print(line[5])
        try:
            row[3]=line[5]['extraPrices'][0]['priceText']
        except:
            print(line[5])
        row[4]=line[5]['price']['priceText']       
        for n in range(len(rowname)):
            if n==1:
                path='./img'+re.search(r'uploaded(.+?)_220x220.jpg',row[1]).group(1).replace('/','_')                
                sheet.insert_image(r,n, path)
            else:
                sheet.write(r,n,row[n])
        sheet.write(r,n+1,row[n+1])
        r=r+1
    workbook.close()

main()
#下载图片
def getImg():
    f=open('img_error.txt','w+',encoding='utf-8',newline='')
    for line in open('detail_list.txt','r',encoding='utf-8'):
        line=eval(line)
        url='https:'+line[1]
        try:
            path='./img'+re.search(r'uploaded(.+?)_220x220.jpg',url).group(1).replace('/','_')
        except:
            print(url)
            raise EnvironmentError
        try:
            if not os.path.exists(path):
                r = requests.get(url,headers=header,timeout=15)
                r.raise_for_status()
                if r.content=="b''":
                    print("爬取失败:"+str(e))
                    return
                # print(r.content)
                # 使用with语句可以不用自己手动关闭已经打开的文件流
                with open(path, "wb") as f:  # 开始写文件，wb代表写二进制文件
                    f.write(r.content)
                print("爬取完成")
            else:
                print("文件已存在")
        except Exception as e:
            print("爬取失败:"+str(e))
# getImg()
    


#爬取详细信息 
# url='https:'+'//detail.tmall.com/item.htm?id=577338910442&areaId=420100&is_b=1&cat_id=2&q=&rn=60fb488bf3da9c64b20d1f67712f2213'
# url='https://detail.tmall.com/item.htm?spm=a220m.1000862.1000725.2.6c1c3580kXLYa5&id=522620395995&areaId=420100&is_b=1&cat_id=2&rn=962e2e84036939cd4b778067429b7a65'




 
