from bs4 import BeautifulSoup
import requests
import csv
from urllib.error import HTTPError
import time
import json
import xlsxwriter

data={
    'session_key':'774334640@qq.com',
    'session_password':'774334640a',
}
# cook='bcookie="v=2&e6b7a84a-9195-4bef-8875-c129bafe2148"; _ga=GA1.2.847762353.1504453393; visit="v=1&M"; JSESSIONID="ajax:0439271021474059911"; liap=true; li_at=AQEDASPXDIUFK84pAAABZnv6oRoAAAFnOg8vNFEAih_Ob97ms3sTDxIbviswdS3aURIuJn0547SVWutyeyO9FaM1vntyG-3kUvDFCt4MPt7Oe63oasfD4Rv7U32VH50OTK6u5EzYZwAdjcGr5DmXx3vt; lang=v=2&lang=zh-cn; li_cc=AQEA_aGhB-shVAAAAWcsfpSmQgP_BNK9H2x9ycQjmNNnhYrmqjkx9jsyz7iR0oWDb-_jmqXHuAU5; spectroscopyId=7fb26e2b-4e07-4e86-9e2c-30629cecf330; _lipt=CwEAAAFnLH6ujXCpFG9gPKV3SqgIb_je4x6T8bPPG3kMDfcdxpyHswIi9yUM6FobhgXgRokJidCGpvsZc_N0XLe4OchCJXOTxlKJXRFVZ_KCIsRVmenAhWtDB3J635q15wsgpoTBWF4eoBzZXgUgSA6D5WiRV_IHA48dQBAH3Bwv3AXDo3qtiY2QRQQIRMVpNEslNu2pzvhmdQEX9uCzylZIU9tTK6rFcTAu1Q; lidc="b=SB05:g=80:u=60:i=1542639978:t=1542723371:s=AQF-34Sr4ale7JAdgL4RUZB4tLNELs5W"'
cook='bcookie="v=2&e6b7a84a-9195-4bef-8875-c129bafe2148"; _ga=GA1.2.847762353.1504453393; bscookie="v=1&201807261153213add1e42-b78f-4d7f-8ac6-bbc3898e2884AQFOkaVBDYFijzw6mAKZ9KzGdtdlQ0Bu"; visit="v=1&M"; JSESSIONID="ajax:0439271021474059911"; liap=true; li_at=AQEDAR-fTEsFejgHAAABaJmWfEcAAAFovaMAR1EAxqnwpsgChLV-B3eb1rrh5gorxXqjZA6TWMkAQWuaRDWeJfuKJfJ0YQ1zdu4bae0fKh4zEBtxCx1VPmcV7hKuvmTdDIrIauvPeWyXsVfWjNbDTTzB; sl=v=1&hZV9g; li_cc=AQGDvjKFyI2w8wAAAWiZln3p2mcGY0evIsTAOVTj844Z-yNwhDWeZ26Gmm2LX3qq7MjEii7ROAH-; lang=v=2&lang=zh-cn; _lipt=CwEAAAFomZaV7McHaBT5nnwnVh5J0mGcFeQsZOTFFtkeqhmOvL6yl3eDijBj7b2A1nj3xasPo_nUFSJPJYVDj48BvvEd4TWhU1Y-nCnlgo7oQmeqv6ioYl8AoVXMAAniyEdqayfQHNRon4HqiVdCHU8VYMBykvXXjTXRBYGS5agyMMHfhQ2sD7wq-SDt0CSEEvcO2VYZ58ObDm-Ecs7kJqoCbJNbhNRm6wINL7VtPE_LWiRdhHye; li_oatml=AQEVRUuKfiRlEQAAAWiZlq3-oVg38cUzricz_ynimu3jjR7c8hSFF9hKu6n0MmgQ_yQzCYjcbAZCOITxnLWdWwnfR0cmUXV8; UserMatchHistory=AQJnRIfyY6BHkQAAAWiZlrp9-H1M0vCvg_eihNBa_fQxW8lSG5nav2n-vov32TJxuEa9BMEuywLd-TM1NLxELW8K6K_aVaGi4C9AW86JUQ; spectroscopyId=90d2db00-42f8-4ad1-8c6b-7dd29b9747f8; lidc="b=SB51:g=51:u=61:i=1548765046:t=1548830222:s=AQG0R7e2jCgyNGfptYlGS7bh4kiNfWzj"'
cook='bcookie="v=2&e6b7a84a-9195-4bef-8875-c129bafe2148"; _ga=GA1.2.847762353.1504453393; bscookie="v=1&201807261153213add1e42-b78f-4d7f-8ac6-bbc3898e2884AQFOkaVBDYFijzw6mAKZ9KzGdtdlQ0Bu"; visit="v=1&M"; JSESSIONID="ajax:0439271021474059911"; liap=true; li_at=AQEDAR-fTEsFejgHAAABaJmWfEcAAAFovaMAR1EAxqnwpsgChLV-B3eb1rrh5gorxXqjZA6TWMkAQWuaRDWeJfuKJfJ0YQ1zdu4bae0fKh4zEBtxCx1VPmcV7hKuvmTdDIrIauvPeWyXsVfWjNbDTTzB; sl=v=1&hZV9g; li_cc=AQGDvjKFyI2w8wAAAWiZln3p2mcGY0evIsTAOVTj844Z-yNwhDWeZ26Gmm2LX3qq7MjEii7ROAH-; lang=v=2&lang=zh-cn; _lipt=CwEAAAFomZaV7McHaBT5nnwnVh5J0mGcFeQsZOTFFtkeqhmOvL6yl3eDijBj7b2A1nj3xasPo_nUFSJPJYVDj48BvvEd4TWhU1Y-nCnlgo7oQmeqv6ioYl8AoVXMAAniyEdqayfQHNRon4HqiVdCHU8VYMBykvXXjTXRBYGS5agyMMHfhQ2sD7wq-SDt0CSEEvcO2VYZ58ObDm-Ecs7kJqoCbJNbhNRm6wINL7VtPE_LWiRdhHye; li_oatml=AQEVRUuKfiRlEQAAAWiZlq3-oVg38cUzricz_ynimu3jjR7c8hSFF9hKu6n0MmgQ_yQzCYjcbAZCOITxnLWdWwnfR0cmUXV8; UserMatchHistory=AQJnRIfyY6BHkQAAAWiZlrp9-H1M0vCvg_eihNBa_fQxW8lSG5nav2n-vov32TJxuEa9BMEuywLd-TM1NLxELW8K6K_aVaGi4C9AW86JUQ; spectroscopyId=90d2db00-42f8-4ad1-8c6b-7dd29b9747f8; lidc="b=SB51:g=51:u=61:i=1548765046:t=1548830222:s=AQG0R7e2jCgyNGfptYlGS7bh4kiNfWzj"'
header={
    'Cookie':cook,
    'csrf-token':'ajax:0439271021474059911',
    'referer':'https://www.linkedin.com/in/annelle-griessel-0b088236/',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
# 'x-li-lang':'zh_CN',
# 'x-li-page-instance':'urn:li:page:d_flagship3_profile_view_base;bX2DBA8ISGSRhuyBkD5VkQ==',
# 'x-li-track':'{"clientVersion":"1.2.6307","osName":"web","timezoneOffset":8,"deviceFormFactor":"DESKTOP","mpName":"voyager-web"}',
# x-restli-protocol-version:2.0.0
}
def get_link():
    f1=open('linkedin_link.txt','r',encoding='utf-8')
    csv_write=csv.writer(f1)
    for i in range(0,106):
        url='https://www.linkedin.com/voyager/api/relationships/connections?start='+str(i*40)+'&count=40&sortType=RECENTLY_ADDED'
        bsObj=requests.get(url,headers=header)
        ele=json.loads(bsObj.text)['elements']
        for e in ele:
            newUrl='https://www.linkedin.com/in/'+e['miniProfile']['publicIdentifier']+'/'
            print(newUrl)
            f1.write(newUrl+'\n')


def get_info():
    f=open('linkedin.txt','a+',encoding='utf-8')
    f_error=open('linkedin_error.txt','a+',encoding='utf-8')
    for line in open('lingying.txt','r',encoding='gb18030'):
        url=line.replace('\n','')
        mainText=url.replace('https://www.linkedin.com/in/','')
        newUrl='https://www.linkedin.com/voyager/api/identity/profiles/'+mainText+'/profileView/'
        # newUrl='https://www.linkedin.com/voyager/api/identity/profiles/'+mainText+'skillCategory?includeHiddenEndorsers=true'
        print(newUrl)
        req=requests.get(newUrl,headers=header)

        if req.status_code!=200:
            
            f_error.write(line)
            
        # print(req.status_code)
        # print([json.loads(req.text)])
        f.write(req.text.replace('\n','').replace('\t','').replace('\r','')+'\n')
        # break
        # time.sleep(3)
        
    f.close()
    
# get_info()

def get_skill(): 
    f=open('linkedin_skill.txt','w+',encoding='utf-8')
    for line in open('linkedin_link.txt','r',encoding='utf-8'):
        url=line
        mainText=url.replace('https://www.linkedin.com/in/','')
        newUrl='https://www.linkedin.com/voyager/api/identity/profiles/'+mainText+'skillCategory?includeHiddenEndorsers=true'
        req=requests.get(newUrl,headers=header)
        f.write(req.text+'\n')
    f.close()

def main():
    f2=open('linkedin_5000','w+',encoding='utf-8',newline='')
    # workbook=xlsxwriter.Workbook('linkedin_modify.xlsx')
    # sheet=workbook.add_worksheet()
    # f=open('linkedin.txt','a+',encoding='utf-8')
    r=0
    f=open('linkedin_link.txt','r',encoding='utf-8')
    f2=open('linkedin_skill.txt','r',encoding='utf-8')
    for line in open('lingying.txt','r',encoding='utf-8'):
        url=line

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
            if 'title' in work:
                workText=workText+work['title']+"_"
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
            if 'locationName' in work:
                workText=workText+work['locationName']
            if 'description' in work:
                workText=workText+work['description']+"\n"
            else:
                workText=workText+"\n"
            

        # print(workText)
        #技能认可
        # print(json.loads(skill_init))
        sk_js=json.loads(skill_init)
        if 'status' in sk_js:
            if sk_js['status']==403:
                url='https://www.linkedin.com/in/annelle-griessel-0b088236/'
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
            if '_deletedFields' in s:
                if s['_deletedFields']==["standardizedSkillUrn", "standardizedSkill"]:
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
        # csv_write.writerow(row)
        # for t in range(len(row)):
        #     sheet.write(r,t,row[t])
        r=r+1
    print(r)    
    # workbook.close()
def get():
    f=open('asd.txt','w+',encoding='utf-8',)
    f1=open('asd1.txt','w+',encoding='utf-8',)
    for line in open('linkedin.txt','r',encoding='utf-8'):
        # f.write(line)
        # break
        if 'positionGroupView"' not in line:
            continue

        js=json.loads(line)
        eduText=""
        for edu in js['educationView']['elements']:

            if 'schoolName' not in edu:
                eduText=eduText+edu['school']['schoolName']+'$'
            else:
                eduText=eduText+edu['schoolName']+'$'
            if 'degreeName' in edu:
                eduText=eduText+edu['degreeName']+'$'
            if 'fieldOfStudy' in edu:
                eduText=eduText+edu['fieldOfStudy']+"$"
            if 'timePeriod' not in edu:
                continue
            if 'startDate' not in edu['timePeriod']:
                continue
            eduText=eduText+str(edu['timePeriod']['startDate']['year'])+'年'
            if 'endDate' in edu['timePeriod']:       
                eduText=eduText+"——"+str(edu['timePeriod']['endDate']['year'])+'年'
            # if 'activities'  in edu:
            #     eduText=eduText+' '+edu['activities']
            # if 'description' in edu:
            #     eduText=eduText+' '+edu['description']
            eduText=eduText+'$'
        # higherDegree=eduText.split('_')[0]
        # print(eduText)
        #工作经历
        workText=""
        nowWork=''
        for wor in js['positionGroupView']['elements']:
            # print(work)
            # break
            # if len(wor['positions'])==2:
            #     f1.write(str(wor))
            #     raise error
            for work in wor['positions']:
                
            # print(len(work['positions']))
                if 'title' in work:
                    workText=workText+work['title']+"$"
                if 'companyName' in work:
                    workText=workText+work['companyName']+'$'
                    
                if 'locationName' in work:
                    workText=workText+work['locationName']+'$'
                try: 
                    if 'startDate' not in work['timePeriod']:
                        continue
                except:
                    continue
                    pass
                    
                workText=workText+str(work['timePeriod']['startDate']['year'])+'年'
                if 'month' in work['timePeriod']['startDate']:
                    workText=workText+str(work['timePeriod']['startDate']['month'])+'月'
                workText=workText+"——"
                if 'endDate' in  work['timePeriod']:
                    workText=workText+str(work['timePeriod']['endDate']['year'])+'年'
                    if 'month' in work['timePeriod']['endDate']:
                        workText=workText+str(work['timePeriod']['endDate']['month'])+'月'+'$'
                    else:
                        workText=workText+'$'
                else:
                    # if 'name' in work:      
                    #     nowWork=nowWork+'_'+work['name']
                    workText=workText+"至今"+'$'



        mini=js['profile']['miniProfile']
        pname=''    
        if 'lastName' in mini:
            pname=mini['lastName']+' '
        pname=pname+mini['firstName']
        print(pname)
        row=[pname,eduText,workText]
    
        f.write(str(row)+'\n')
    f.close()
    # break


# for line in open('asd.txt','r',encoding='utf-8',):
#     print(line)
#     break
workbook = xlsxwriter.Workbook('领英.xlsx') #创建工作簿
sheet = workbook.add_worksheet()
r=0
for line in open('asd.txt','r',encoding='utf-8'):
    line=eval(line)
    for m in range(3):
        sheet.write(r,m,line[m])
    r=r+1
print(r)
workbook.close()