from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp
import time
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# https://www.linkedin.com/uas/login-submit
data={
    'session_key':'774334640@qq.com',
    'session_password':'774334640a',
# session_redirect:/voyager/loginRedirect.html
}
# loginUrl='https://www.linkedin.com/uas/login-submit'
# response=requests.post(loginUrl,data)
# print(response.text)
# token=json.loads(response.text)['data']['token']

cook='bcookie="v=2&e6b7a84a-9195-4bef-8875-c129bafe2148"; _ga=GA1.2.847762353.1504453393; bscookie="v=1&201807261153213add1e42-b78f-4d7f-8ac6-bbc3898e2884AQFOkaVBDYFijzw6mAKZ9KzGdtdlQ0Bu"; _lipt=CwEAAAFmetGb8e8zfPHZXUKk8T5chfEm42WW2VDJxQBtHvI63jLipwt6jZ00MY26ex1y6lEUQE7iiZ3n7fwBOkmtifNHHaVGPFWAoVQkGrBdQZEYy3Uxr1qKiYDsGHqFUCne_DIqODbMZmgUllcFfUjCltSqLcCUoGCcfZfKNzHCmGHrICGv-e5YT_AkKnHxpQWpIMbqLBun7MkOrhCege-6UkLg5Ua1FgMNGJvarsk; _guid=9af84474-c269-4173-ad7c-8c3766235272; li_oatml=AQEnFngsmPWikAAAAWZ60ba6koy90ih2OSpHlxuAlurNTdu_h9Dy2pudGt5qd7NRXMSL0gZ-e3Wx_p5AHLwXez1Wp_-hekEw; visit="v=1&M"; lang="v=2&lang=zh-cn"; JSESSIONID="ajax:0439271021474059911"; leo_auth_token="GST:8iKDsYRKFGGkEzphVZ0G7YA0uYP_cfypNrLDhdTKUDDgEAhFonbQdt:1539678314:e225e4638fff38caac331ab2321e9efea0dc1281"; li_at=AQEDASPXDIUFK84pAAABZnv6oRoAAAFmoAclGlEANJSsupIwhpchZ5lUeBXhif0lSUMVJRV_XYcw2ZU9kxEmxS6cSTjZiRtnVs8Uby191URFPfcM2u4Cwq3qKV9aXo6axaSihiqpUCHUv05rOXPHAnab; liap=true; li_cc=AQHh_CVcMTIb4wAAAWZ7-8F7TmJ9H4KXdrFRYUQZsv2D1aoYyC3QxoIovTvSdphJ3YZ_dXwd1fLF; lidc="b=SGST00:g=6:u=1:i=1539678549:t=1539764949:s=AQF6BkkW6ia13YwX_TKYH9JId2uSMJ09"'

header={
    'Cookie':cook,
    # 'referer':'https://www.linkedin.com/mynetwork/invite-connect/connections/',
    'csrf-token':'ajax:0439271021474059911',
}
# f1=open('linkedin.csv','a+',encoding='gb18030',newline='')
# csv_write=csv.writer(f1)
# for i in range(103,106):
#     url='https://www.linkedin.com/voyager/api/relationships/connections?start='+str(i*40)+'&count=40&sortType=RECENTLY_ADDED'
#     bsObj=requests.get(url,headers=header)
#     ele=json.loads(bsObj.text)['elements']
#     for e in ele:
#         # print(e['miniProfile'])
#         newUrl='https://www.linkedin.com/in/'+e['miniProfile']['publicIdentifier']+'/'
#         print(newUrl)
#         csv_write.writerow([newUrl])
#     #     print(bsObj)
#     #     # profileView='https://www.linkedin.com/voyager/api/identity/profiles/%E9%BB%98-%E5%BC%A0-778261149/profileView/'
#     #     break
#     # break

f2=open('linkedin_final.csv','a+',encoding='gb18030',newline='')
csv_write=csv.writer(f2)

for line in csv.reader(open('linkedin.csv','r',encoding='gb18030')):
    url=line[0]
    print(url)
    # url='https://www.linkedin.com/in/贵勇-游-67051615b/'
    mainText=url.replace('https://www.linkedin.com/in/','')
    newUrl='https://www.linkedin.com/voyager/api/identity/profiles/'+mainText+'profileView/'
    req=requests.get(newUrl,headers=header)
    js=json.loads(req.text)
    # print(js)
    #教育背景
    if 'educationView' not in js:
        continue
    eduText=""
    for edu in js['educationView']['elements']:
        if 'schoolName' not in edu:
            eduText=eduText+edu['school']['schoolName']+'_'
        else:
            eduText=eduText+edu['schoolName']+'_'
        if 'degreeName' in edu:
            eduText=eduText+edu['degreeName']+'_'
        if 'fieldOfStudy' in edu:
            eduText=eduText+edu['fieldOfStudy']+"&nbsp;"
        if 'timePeriod' not in edu:
            continue
        if 'startDate' not in edu['timePeriod']:
            continue
        eduText=eduText+str(edu['timePeriod']['startDate']['year'])+'年'
        if 'endDate' in edu['timePeriod']:       
            eduText=eduText+"——"+str(edu['timePeriod']['endDate']['year'])+'年'
        eduText=eduText+'\n'
    higherDegree=eduText.split('_')[0]
    # print(eduText)
    #工作经历
    workText=""
    nowWork=''
    for work in js['positionGroupView']['elements']:
        # print(work)
        # break
        if 'title' in work['positions'][0]:
            workText=workText+work['positions'][0]['title']+"_"
        if 'name' in work:
            workText=workText+work['name']+'&nbsp;'
        if 'startDate' not in work['timePeriod']:
            continue
        workText=workText+str(work['timePeriod']['startDate']['year'])+'年'
        if 'month' in work['timePeriod']['startDate']:
            workText=workText+str(work['timePeriod']['startDate']['month'])+'月'
        workText=workText+"——"
        if 'endDate' in  work['timePeriod']:
            workText=workText+str(work['timePeriod']['endDate']['year'])+'年'
            if 'month' in work['timePeriod']['endDate']:
                workText=workText+"-"+str(work['timePeriod']['endDate']['month'])+'月'+'&nbsp'
            else:
                workText=workText+'&nbsp'
        else:
            if 'name' in work:      
                nowWork=nowWork+'_'+work['name']
            workText=workText+"至今"+'&nbsp'
        if 'locationName' in work['positions'][0]:
            workText=workText+work['positions'][0]['locationName']
        workText=workText+"\n"
    # print(workText)
    #技能认可
    skillText=''
    # print(js['skillView']['elements'])
    for skill in js['skillView']['elements']:
        skillText=skillText+skill['name']+'_'
    # print(skillText)
    try:
        summary=js['profile']['summary']
    except:
        summary=''
    mini=js['profile']['miniProfile']
    pname=''
    if 'lastName' in mini:
        pname=pname+mini['lastName']
    pname=pname+mini['firstName']
    if 'occupation' in mini:
        
        occupation=mini['occupation']
    else:
        occupation=''
    if 'locationName' in js['profile']:
        city=js['profile']['locationName']
    else:
        city=''
    row=[url,pname,occupation,city,nowWork,higherDegree,summary,workText,eduText,skillText]
    csv_write.writerow(row)
    # break
        
    







#可用来解决js渲染的重定向数据抓取不到问题
def phangetObj(url,data=None):
    desire = DesiredCapabilities.PHANTOMJS.copy() 
    for key, value in header.items(): 
        desire['phantomjs.page.customHeaders.{}'.format(key)] = value 
    driver = webdriver.PhantomJS(desired_capabilities=desire, executable_path="phantomjs.exe",service_args=['--load-images=no'])#将yes改成no可以让浏览器不加载图片 
    # driver =webdriver.PhantomJS()   
    #使用浏览器请求页面
    driver.get(url)
    # driver.add_cookie(header)
    #加载3秒，等待所有数据加载完毕
    time.sleep(3)
    #通过id来定位元素，
    #.text获取元素的文本数据
    # dl=driver.find_elements_by_css_selector("#searchLeftOptions")
    # dl=driver.find_element_by_id("bpr-guid-1537650").get_text()
    # print(dl)
    
    pageSource=driver.page_source
    print(pageSource)
    # bsObj=BeautifulSoup(pageSource,"html.parser")
    # education=bsObj.find('code',{'id':'bpr-guid-1537650'}).get_text()
    # data=json.loads(education)['data']
    # print(data)
    driver.close()
    return 0
# phangetObj(newUrl)
