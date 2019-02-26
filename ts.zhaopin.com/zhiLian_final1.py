
import requests
from bs4  import BeautifulSoup
import json
import time
import xlsxwriter

position=input('请输入职位名称：')
page=int(input('请输入爬取页码：'))
# https://sou.zhaopin.com/?p=2&jl=535&kw=%E9%A2%84%E7%AE%97%E5%91%98&kt=3&sf=0&st=0

header={
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://sou.zhaopin.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

def get_obj(url):
    for  m in range(3):
        try:
            req=requests.get(url,headers=header,timeout=10)
            req.encoding='utf-8'
            bsObj=BeautifulSoup(req.text,'html.parser')
            return bsObj
        except:
            time.sleep(5)
            # continue
    return None

now=time.strftime('%Y.%m.%d',time.localtime(time.time()))
workbook = xlsxwriter.Workbook(position+str(now)+'.xlsx') #创建工作簿
sheet = workbook.add_worksheet()
rowname=['企业名称','地区','企业类型','规模','地址','经营范围','网址','电话号码','电话号码（更多号码）','归类','招聘信息','发布时间']
for c in range(len(rowname)):
    sheet.write(0,c,rowname[c])
r=1
for i in range(page):
    print('开始爬第'+str(i+1)+'页...')
    url='https://fe-api.zhaopin.com/c/i/sou?start='+str(i*90)+'&pageSize=90&cityId=535&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw='+str(position)+'&kt=3&at=f8b51268d1fd4981b753859dc78a4f8c&rt=4167f6cc414d47e5846fe1c00e47dfbe&_v=0.49487354&userCode=691899259&x-zp-page-request-id=cd7bf1a971f24c5389072109b8cec29b-1550921203387-419462'
    try:
        req=requests.get(url,headers=header)
        js=json.loads(req.text)['data']['results']
    except:
        print('职位名称为中文汉字，请重新运行程序')
        break
    for j in js:
        id=j['SOU_POSITION_ID']
        url1='https://jobs.zhaopin.com/'+id+'.htm'
        print(url1)
        bsObj=get_obj(url1)
        if bsObj==None:
            print(url+'  error')
            continue
        # print(j['city'],j['jobName'])  
        companyName=''
        size=''
        tp=''
        person=''
        companyUrl=''
        address=''

        companyName=j['company']['name']
        size=j['company']['size']['name']
        city=j['city']['display']
        ul=bsObj.find('ul',class_='promulgator-ul cl')
        job_detail=''
        try:
            job_detail=job_detail+j['jobName']
        except:
            pass
        # try:
        #     job_detail=job_detail+j['salary']+','
        # except:
        #     pass
        # try:
        #     job_detail=job_detail+j['city']['display']+','
        # except:
        #     pass
        # try:
        #     job_detail=job_detail+j['workingExp']['name']+','
        # except:
        #     pass
        # try:
        #     job_detail=job_detail+j['eduLevel']['name']+','
        # except:
        #     pass
        # try:
        #     job_detail=job_detail+'、'.join(j['welfare'])+','
        # except:
        #     pass
        updateDate=''
        try:
            updateDate=j['updateDate']
        except:
            pass

        if ul!=None:
            lilist=ul.find_all('li')
            for li in lilist:
                if 'icon-promulgator-type' in  li.find('span').get('class'):
                    tp=li.get_text()
                    continue
                if 'icon-promulgator-person' in  li.find('span').get('class'):
                    person=li.get_text()
                    continue
                if 'icon-promulgator-link' in  li.find('span').get('class'):
                    size=li.get_text().replace('\n','')
                    continue
                if 'icon-promulgator-url' in  li.find('span').get('class'):
                    companyUrl=li.get_text().replace('\n','')
                    continue
                if 'icon-promulgator-addres'  in  li.find('span').get('class'):
                    address=li.get_text().replace('\n','')
                    continue   
        row=[companyName,city,tp,size,address,person,companyUrl,'','','',job_detail ,updateDate]    
        # print(row)
        for c in range(len(row)):
            sheet.write(r,c,row[c])
        r=r+1
        # break
    # break
workbook.close()
# print(len(js))