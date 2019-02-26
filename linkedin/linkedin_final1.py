from bs4 import BeautifulSoup
import requests
import csv
from urllib.error import HTTPError
import time
import json
import xlsxwriter

# https://www.linkedin.com/uas/login-submit
data={
    'session_key':'774334640@qq.com',
    'session_password':'774334640a',
}
# loginUrl='https://www.linkedin.com/uas/login-submit'
# response=requests.post(loginUrl,data)
# print(response.text)
# token=json.loads(response.text)['data']['token']

# cook='bcookie="v=2&e6b7a84a-9195-4bef-8875-c129bafe2148"; _ga=GA1.2.847762353.1504453393; bscookie="v=1&201807261153213add1e42-b78f-4d7f-8ac6-bbc3898e2884AQFOkaVBDYFijzw6mAKZ9KzGdtdlQ0Bu"; _lipt=CwEAAAFmetGb8e8zfPHZXUKk8T5chfEm42WW2VDJxQBtHvI63jLipwt6jZ00MY26ex1y6lEUQE7iiZ3n7fwBOkmtifNHHaVGPFWAoVQkGrBdQZEYy3Uxr1qKiYDsGHqFUCne_DIqODbMZmgUllcFfUjCltSqLcCUoGCcfZfKNzHCmGHrICGv-e5YT_AkKnHxpQWpIMbqLBun7MkOrhCege-6UkLg5Ua1FgMNGJvarsk; _guid=9af84474-c269-4173-ad7c-8c3766235272; li_oatml=AQEnFngsmPWikAAAAWZ60ba6koy90ih2OSpHlxuAlurNTdu_h9Dy2pudGt5qd7NRXMSL0gZ-e3Wx_p5AHLwXez1Wp_-hekEw; visit="v=1&M"; lang="v=2&lang=zh-cn"; JSESSIONID="ajax:0439271021474059911"; leo_auth_token="GST:8iKDsYRKFGGkEzphVZ0G7YA0uYP_cfypNrLDhdTKUDDgEAhFonbQdt:1539678314:e225e4638fff38caac331ab2321e9efea0dc1281"; li_at=AQEDASPXDIUFK84pAAABZnv6oRoAAAFmoAclGlEANJSsupIwhpchZ5lUeBXhif0lSUMVJRV_XYcw2ZU9kxEmxS6cSTjZiRtnVs8Uby191URFPfcM2u4Cwq3qKV9aXo6axaSihiqpUCHUv05rOXPHAnab; liap=true; li_cc=AQHh_CVcMTIb4wAAAWZ7-8F7TmJ9H4KXdrFRYUQZsv2D1aoYyC3QxoIovTvSdphJ3YZ_dXwd1fLF; lidc="b=SGST00:g=6:u=1:i=1539678549:t=1539764949:s=AQF6BkkW6ia13YwX_TKYH9JId2uSMJ09"'
# cook='bcookie="v=2&e6b7a84a-9195-4bef-8875-c129bafe2148"; _ga=GA1.2.847762353.1504453393; visit="v=1&M"; JSESSIONID="ajax:0439271021474059911"; liap=true; li_at=AQEDASPXDIUFK84pAAABZnv6oRoAAAFnOg8vNFEAih_Ob97ms3sTDxIbviswdS3aURIuJn0547SVWutyeyO9FaM1vntyG-3kUvDFCt4MPt7Oe63oasfD4Rv7U32VH50OTK6u5EzYZwAdjcGr5DmXx3vt; lang=v=2&lang=zh-cn; li_cc=AQEA_aGhB-shVAAAAWcsfpSmQgP_BNK9H2x9ycQjmNNnhYrmqjkx9jsyz7iR0oWDb-_jmqXHuAU5; spectroscopyId=7fb26e2b-4e07-4e86-9e2c-30629cecf330; _lipt=CwEAAAFnLH6ujXCpFG9gPKV3SqgIb_je4x6T8bPPG3kMDfcdxpyHswIi9yUM6FobhgXgRokJidCGpvsZc_N0XLe4OchCJXOTxlKJXRFVZ_KCIsRVmenAhWtDB3J635q15wsgpoTBWF4eoBzZXgUgSA6D5WiRV_IHA48dQBAH3Bwv3AXDo3qtiY2QRQQIRMVpNEslNu2pzvhmdQEX9uCzylZIU9tTK6rFcTAu1Q; lidc="b=SB05:g=80:u=60:i=1542640944:t=1542723371:s=AQGF9YbQ8DTqh06gi--2yaM5Y_lbjJL6"'
cook='bcookie="v=2&e6b7a84a-9195-4bef-8875-c129bafe2148"; _ga=GA1.2.847762353.1504453393; visit="v=1&M"; JSESSIONID="ajax:0439271021474059911"; liap=true; li_at=AQEDASPXDIUFK84pAAABZnv6oRoAAAFnOg8vNFEAih_Ob97ms3sTDxIbviswdS3aURIuJn0547SVWutyeyO9FaM1vntyG-3kUvDFCt4MPt7Oe63oasfD4Rv7U32VH50OTK6u5EzYZwAdjcGr5DmXx3vt; lang=v=2&lang=zh-cn; li_cc=AQEA_aGhB-shVAAAAWcsfpSmQgP_BNK9H2x9ycQjmNNnhYrmqjkx9jsyz7iR0oWDb-_jmqXHuAU5; spectroscopyId=7fb26e2b-4e07-4e86-9e2c-30629cecf330; _lipt=CwEAAAFnLH6ujXCpFG9gPKV3SqgIb_je4x6T8bPPG3kMDfcdxpyHswIi9yUM6FobhgXgRokJidCGpvsZc_N0XLe4OchCJXOTxlKJXRFVZ_KCIsRVmenAhWtDB3J635q15wsgpoTBWF4eoBzZXgUgSA6D5WiRV_IHA48dQBAH3Bwv3AXDo3qtiY2QRQQIRMVpNEslNu2pzvhmdQEX9uCzylZIU9tTK6rFcTAu1Q; lidc="b=SB05:g=80:u=60:i=1542639978:t=1542723371:s=AQF-34Sr4ale7JAdgL4RUZB4tLNELs5W"'
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

f2=open('linkedin_final_modify.csv','w+',encoding='gb18030',newline='')
csv_write=csv.writer(f2)
# workbook=xlsxwriter.Workbook('linkedin_modify.xlsx')
# sheet=workbook.add_worksheet()
# f=open('linkedin.txt','a+',encoding='utf-8')
r=0
f=open('linkedin - 副本.txt','r',encoding='gb18030')
f2=open('linkedin_skill.txt','r',encoding='utf-8')
for line in open('linkedin.txt','r',encoding='utf-8'):
    url=f.readline()
    skill_init=f2.readline()
    print(url)
    # r=r+1
    # url=line[0]
    # print(url)
    # # url='https://www.linkedin.com/in/贵勇-游-67051615b/'
    # mainText=url.replace('https://www.linkedin.com/in/','')
    # mainText='卫国-孙-252418109/'
    # newUrl='https://www.linkedin.com/voyager/api/identity/profiles/'+mainText+'profileView/'
    # newUrl='https://www.linkedin.com/voyager/api/identity/profiles/'+mainText+'skillCategory?includeHiddenEndorsers=true'
    # http://www.linkedin.com/voyager/api/identity/profiles/%E5%8D%AB%E5%9B%BD-%E5%AD%99-252418109/skillCategory?includeHiddenEndorsers=true
    # +'memberConnections?q\u003Dconnections/'
    # print(newUrl)
    # # break
    # req=requests.get(newUrl,headers=header)
    # print(req.text)
    # break
    # # print(js)
    # f.write(req.text+'\n')
    # continue
    # print(js)
    #教育背景
    js=json.loads(line)

    if 'educationView' not in js:
        #重新写js
        # time.sleep(3)        
        mainText=url.replace('https://www.linkedin.com/in/','')
        newUrl='https://www.linkedin.com/voyager/api/identity/profiles/'+mainText+'profileView/'
        req=requests.get(newUrl,headers=header)
        js=json.loads(req.text)
        print(url)
        print('重新获取')  
        time.sleep(3)        
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
        if 'activities'  in edu:
            eduText=eduText+' '+edu['activities']
        if 'description' in edu:
            eduText=eduText+' '+edu['description']
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
        if 'description' in work['positions'][0]:
            workText=workText+work['positions'][0]['description']+"\n"
        else:
            workText=workText+"\n"
        

    # print(workText)
    #技能认可
    # print(json.loads(skill_init))
    sk_js=json.loads(skill_init)
    if 'status' in sk_js:
        if sk_js['status']==403:
            mainText=url.replace('https://www.linkedin.com/in/','')
            newUrl='https://www.linkedin.com/voyager/api/identity/profiles/'+mainText+'skillCategory?includeHiddenEndorsers=true'
            req=requests.get(newUrl,headers=header)
            sk_js=json.loads(req.text)
            print(url)
            print('重新获取')  
            time.sleep(3) 
            
    if 'elements' in sk_js:
        sk=sk_js['elements']
    elif 'included' in sk_js:
        sk=sk_js['included']   
    else:
        print(json.loads(skill_init))
        # raise error
        continue
        
 
    skillText=''
    
    for s in sk:
        if '$deletedFields' in s:
            if s['$deletedFields']==["standardizedSkillUrn", "standardizedSkill"]:
                skillText=skillText+s['name']+'_'
        else:
            break
    for s in sk:    
        if 'endorsedSkills' in s:
            for m in s['endorsedSkills']:
                skillText=skillText+m['skill']['name']+'_'
        else:
            break
    
    # # print(js['skillView']['elements'])
    # for skill in js['skillView']['elements']:
    #     skillText=skillText+skill['name']+'_'
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
    # print(row)
    csv_write.writerow(row)
    # for t in range(len(row)):
    #     sheet.write(r,t,row[t])



    r=r+1
print(r)    
# workbook.close()
# 