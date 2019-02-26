import requests
from bs4 import BeautifulSoup
import base64
import json
import xlrd
import time
import xlsxwriter



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

def get_link():
    j=0
    f=open('desease_link.txt','a+',encoding='utf-8')
    for line in open('desease.txt','r',encoding='utf-8'):
        print(j)
        line=eval(line)
        print(line[3])
        url='https://baike.baidu.com/search/none?word='+str(line[3])+'&pn=0&rn=10&enc=utf8'
        for  m in range(3):
            try:
                req=requests.get(url,headers=header,allow_redirects=False,timeout=10)
                req.encoding='utf-8'
                bsObj=BeautifulSoup(req.text,'html.parser')
            except:
                time.sleep(5)
                # continue
        try:
            ddlist=bsObj.find('dl',class_='search-list').find_all('dd')
        except:
            continue
        le=len(ddlist)
        print('条数：'+str(le))
        for i in range(le):
            dd=ddlist[i]
            a=dd.find('a')
            row=[line[3]]+[a.attrs['href'],a.get_text()]+line
            f.write(str(row)+'\n')
        j=j+1
        # time.sleep(1)
        if j==4350:
            break
    f.close()

def get_detail():
    cook='BAIDUID=C8730DDCADF6648A2A22D8137B706A70:FG=1; BIDUPSID=C8730DDCADF6648A2A22D8137B706A70; PSTM=1548486368; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1550546962; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1550546962; BDUSS=GduU2htdW1VNmZ6WXhsMWU4MG40ZkVFbDBkTkVrWkcxd1N6bVAtd1ZDM3ZEWk5jQUFBQUFBJCQAAAAAAAAAAAEAAABmUMViY2hhbmcyMjI3MDEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO-Aa1zvgGtcT; BDSFRCVID=Uz_OJeC6262-vdn9evRkhixg4cb5q0OTH6aoOJt3j6yuKGXH6bcnEG0PjU8g0Ku-J0QOogKKLgOTHULF_2uxOjjg8UtVJeC6EG0P3J; H_BDCLCKID_SF=tRk8oKPyJKvhKROmK4r2q4tehHRM0pOeWDTm5-nTthcIHC0wbt6IK6jB2MjlLhQbL6chBlvlylI5OCFRjTAKD63BeUbX-I6E2I6yQnT8HJOoDDv5bjOcy4LdjG5Q0njMB5F804nDapk-EtoIhJr5K6Ku3-Aq54RXKHR0LhTOf4T6qJbs34IbQfbQ0MoPqP-jW5ILaDJlBb7JOpvsbUnxyhLTQRPH-Rv92DQMVU52QqcqEIQHQT3mDUThDHAftTKDtbusL-35HDK2hb-kht_3hPPvXP6-35KHbbnR_x54fR5Wqt3ojxQKb4cXyUrIBq37JD6y2664KDoDDKJYMTKBXbcLXPoxJpORBRbMopvaKf7FjUcvbURvX--g3-7PWU5dtjTO2bc_5KnlfMQ_bf--QfbQ0abZqj_efnCe_C_QKRI_HRjYbb__-P4DentD0fRZ5mAqoDbpHlcSMCTNK5QoM-FbbNOMBMneWI7naIQqWl3tSp6mQR8b-609WJ_jbDr43bRTKnLy5KJvfj6bDxoahP-UyPvMWh37QmJlMKoaMp78jR093JO4y4Ldj4oxJp8eWJLD_KIMJIIhbP365IT0M-_eKMrXetJyaROeBR-BtC_ahDDRe505JRL3hJne2bQHKKI_3JjV5P52HPJuJRoMhq4DbfO0-4u_K5RJV-0yH4OkeqOJ2Mt5y4Ce0Gr--qj0Q-DqWp6vBJT8ExjRetLabjtpeG-fqTDHJnFs3br2HtcsHJ7xMtI_-P4DenoEyMRZ5mAqoDL-H4QfDCTN5l5OM-FbbNO25jQDtgOnaIQqah7kfKOFjRrhyU-Ryaja5-643bRTBfKy5KJvfj6_DhQchP-UyPvMWh37QmJlMKoaMp78jR093JO4y4Ldj4oxJp8eWJQ2QJ8BtKLabKJP; delPer=0; PSINO=1; H_PS_PSSID=1457_21124'
    header={
        'Cookie':cook,
        'Host': 'baike.baidu.com',
        'Referer': 'https://baike.baidu.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    f=open('de_detail_first.txt','a+',encoding='utf-8')
    root='https://baike.baidu.com'
    for line in open('de_first.txt','r',encoding='utf-8'):
        line=eval(line)
        if 'http' in line[1]:
            url=line[1]
        else:
            url=root +line[1]
        print(url)
        for  m in range(3):
            try:
                req=requests.get(url,headers=header,allow_redirects=False,timeout=10)
                req.encoding='utf-8'
                bsObj=BeautifulSoup(req.text,'html.parser')
                break
            except:
                time.sleep(5)
                # continue
        row=line[:3]+[str(bsObj).replace('\n','')]+line[3:]
        f.write(str(row)+'\n')
    f.close()

def sort_out():
    cook='BAIDUID=C8730DDCADF6648A2A22D8137B706A70:FG=1; BIDUPSID=C8730DDCADF6648A2A22D8137B706A70; PSTM=1548486368; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1550546962; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1550546962; BDUSS=GduU2htdW1VNmZ6WXhsMWU4MG40ZkVFbDBkTkVrWkcxd1N6bVAtd1ZDM3ZEWk5jQUFBQUFBJCQAAAAAAAAAAAEAAABmUMViY2hhbmcyMjI3MDEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO-Aa1zvgGtcT; BDSFRCVID=Uz_OJeC6262-vdn9evRkhixg4cb5q0OTH6aoOJt3j6yuKGXH6bcnEG0PjU8g0Ku-J0QOogKKLgOTHULF_2uxOjjg8UtVJeC6EG0P3J; H_BDCLCKID_SF=tRk8oKPyJKvhKROmK4r2q4tehHRM0pOeWDTm5-nTthcIHC0wbt6IK6jB2MjlLhQbL6chBlvlylI5OCFRjTAKD63BeUbX-I6E2I6yQnT8HJOoDDv5bjOcy4LdjG5Q0njMB5F804nDapk-EtoIhJr5K6Ku3-Aq54RXKHR0LhTOf4T6qJbs34IbQfbQ0MoPqP-jW5ILaDJlBb7JOpvsbUnxyhLTQRPH-Rv92DQMVU52QqcqEIQHQT3mDUThDHAftTKDtbusL-35HDK2hb-kht_3hPPvXP6-35KHbbnR_x54fR5Wqt3ojxQKb4cXyUrIBq37JD6y2664KDoDDKJYMTKBXbcLXPoxJpORBRbMopvaKf7FjUcvbURvX--g3-7PWU5dtjTO2bc_5KnlfMQ_bf--QfbQ0abZqj_efnCe_C_QKRI_HRjYbb__-P4DentD0fRZ5mAqoDbpHlcSMCTNK5QoM-FbbNOMBMneWI7naIQqWl3tSp6mQR8b-609WJ_jbDr43bRTKnLy5KJvfj6bDxoahP-UyPvMWh37QmJlMKoaMp78jR093JO4y4Ldj4oxJp8eWJLD_KIMJIIhbP365IT0M-_eKMrXetJyaROeBR-BtC_ahDDRe505JRL3hJne2bQHKKI_3JjV5P52HPJuJRoMhq4DbfO0-4u_K5RJV-0yH4OkeqOJ2Mt5y4Ce0Gr--qj0Q-DqWp6vBJT8ExjRetLabjtpeG-fqTDHJnFs3br2HtcsHJ7xMtI_-P4DenoEyMRZ5mAqoDL-H4QfDCTN5l5OM-FbbNO25jQDtgOnaIQqah7kfKOFjRrhyU-Ryaja5-643bRTBfKy5KJvfj6_DhQchP-UyPvMWh37QmJlMKoaMp78jR093JO4y4Ldj4oxJp8eWJQ2QJ8BtKLabKJP; delPer=0; PSINO=1; H_PS_PSSID=1457_21124'
    header={
        'Cookie':cook,
        'Host': 'baike.baidu.com',
        'Referer': 'https://baike.baidu.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    workbook = xlsxwriter.Workbook('疾病2'+'.xlsx') #创建工作簿
    sheet = workbook.add_worksheet()
    r=0
    f=open('de_final.txt','w+',encoding='utf-8')
    rowname=['名称','疾病信息','概况','病因','症状','诊断','治疗','预防','生活影响（环境、饮食）','',]
    for line in open('de_detail_first.txt','r',encoding='utf-8'):
        line=eval(line)
        # print(line[2])
        # break
        n=-1
        bsObj=BeautifulSoup(line[3],'html.parser')
        try:
            summary=bsObj.find('div',class_='lemma-summary').get_text()
        except:
            print(line[2])
            continue
        othername=bsObj.find('div',class_='basic-info cmn-clearfix')
        othername=str(othername).replace('</dt',':</dt')
        othername=str(othername).replace('</dd','   \n</dd')
        othername=BeautifulSoup(othername,'html.parser').get_text()
        #找到 
        row=[line[2].replace('_百度百科',''),othername,summary]

        divlist=bsObj.find('div',class_='main-content').find_all('div')
        for div in divlist:
            if div.get('class')==None:
                continue
            # print(div.get('class'))
            if 'para-title' in  div.get('class') and 'level-2' in  div.get('class'):
                ti_re=div.find('span',class_='title-prefix').get_text()
                title=div.find('h2',class_='title-text').get_text().replace(ti_re,'')
                n=-1

                for h in range(len(rowname)):
                    special='特病简预防因症诊断检养治疗饮食环境生活影响'
                    for l in range(len(special)):
                        if special[l] in title and special[l] in rowname[h]:
                            n=h
                            break                    
                if n==-1:
                    if title in rowname:
                        n=rowname.index(title)
                    else:
                        rowname.append(title)
                        n=rowname.index(title)
                    if n>len(row)-1:
                        row=row+['' for t in range(n-len(row)+1)]
                    row[n]=row[n]+title+':'
            elif 'para-title' in  div.get('class') and 'level-2' not in  div.get('class'):
                if n>len(row)-1:
                   row=row+['' for t in range(n-len(row)+1)]
                row[n]=row[n]+div.get_text()+'\n'   
            elif 'para' in  div.get('class') and n!=-1:
                if n>len(row)-1:
                    row=row+['' for t in range(n-len(row)+1)]
                row[n]=row[n]+div.get_text()+'\n'

            else:
                pass
        for j in range(len(row)):
            sheet.write(r,j,row[j])
        r=r+1
        # break

    for j in range(len(rowname)):
        sheet.write(r,j,rowname[j])
    workbook.close()
sort_out()

def sort_out1():
    cook='BAIDUID=C8730DDCADF6648A2A22D8137B706A70:FG=1; BIDUPSID=C8730DDCADF6648A2A22D8137B706A70; PSTM=1548486368; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1550546962; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1550546962; BDUSS=GduU2htdW1VNmZ6WXhsMWU4MG40ZkVFbDBkTkVrWkcxd1N6bVAtd1ZDM3ZEWk5jQUFBQUFBJCQAAAAAAAAAAAEAAABmUMViY2hhbmcyMjI3MDEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO-Aa1zvgGtcT; BDSFRCVID=Uz_OJeC6262-vdn9evRkhixg4cb5q0OTH6aoOJt3j6yuKGXH6bcnEG0PjU8g0Ku-J0QOogKKLgOTHULF_2uxOjjg8UtVJeC6EG0P3J; H_BDCLCKID_SF=tRk8oKPyJKvhKROmK4r2q4tehHRM0pOeWDTm5-nTthcIHC0wbt6IK6jB2MjlLhQbL6chBlvlylI5OCFRjTAKD63BeUbX-I6E2I6yQnT8HJOoDDv5bjOcy4LdjG5Q0njMB5F804nDapk-EtoIhJr5K6Ku3-Aq54RXKHR0LhTOf4T6qJbs34IbQfbQ0MoPqP-jW5ILaDJlBb7JOpvsbUnxyhLTQRPH-Rv92DQMVU52QqcqEIQHQT3mDUThDHAftTKDtbusL-35HDK2hb-kht_3hPPvXP6-35KHbbnR_x54fR5Wqt3ojxQKb4cXyUrIBq37JD6y2664KDoDDKJYMTKBXbcLXPoxJpORBRbMopvaKf7FjUcvbURvX--g3-7PWU5dtjTO2bc_5KnlfMQ_bf--QfbQ0abZqj_efnCe_C_QKRI_HRjYbb__-P4DentD0fRZ5mAqoDbpHlcSMCTNK5QoM-FbbNOMBMneWI7naIQqWl3tSp6mQR8b-609WJ_jbDr43bRTKnLy5KJvfj6bDxoahP-UyPvMWh37QmJlMKoaMp78jR093JO4y4Ldj4oxJp8eWJLD_KIMJIIhbP365IT0M-_eKMrXetJyaROeBR-BtC_ahDDRe505JRL3hJne2bQHKKI_3JjV5P52HPJuJRoMhq4DbfO0-4u_K5RJV-0yH4OkeqOJ2Mt5y4Ce0Gr--qj0Q-DqWp6vBJT8ExjRetLabjtpeG-fqTDHJnFs3br2HtcsHJ7xMtI_-P4DenoEyMRZ5mAqoDL-H4QfDCTN5l5OM-FbbNO25jQDtgOnaIQqah7kfKOFjRrhyU-Ryaja5-643bRTBfKy5KJvfj6_DhQchP-UyPvMWh37QmJlMKoaMp78jR093JO4y4Ldj4oxJp8eWJQ2QJ8BtKLabKJP; delPer=0; PSINO=1; H_PS_PSSID=1457_21124'
    header={
        'Cookie':cook,
        'Host': 'baike.baidu.com',
        'Referer': 'https://baike.baidu.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    workbook = xlsxwriter.Workbook('疾病初版2'+'.xlsx') #创建工作簿
    sheet = workbook.add_worksheet()
    r=0
    f=open('de_final.txt','w+',encoding='utf-8')
    rowname=['name','othername','name1']
    for j in range(len(rowname)):
        sheet.write(r,j,rowname[j])
    for line in open('de_detail_first.txt','r',encoding='utf-8'):
        line=eval(line)

        n=-1
        bsObj=BeautifulSoup(line[3],'html.parser')
        try:
            summary=bsObj.find('div',class_='lemma-summary').get_text()
        except:
            print(line[2])
            continue
        othername=bsObj.find('div',class_='basic-info cmn-clearfix')
        othername=str(othername).replace('</dt',':</dt')
        othername=str(othername).replace('</dd','   \n</dd')
        othername=BeautifulSoup(othername,'html.parser').get_text()
        #找到 
        row=[line[2].replace('_百度百科',''),othername,summary]+['' for u in range(20)]
        n=2
        divlist=bsObj.find('div',class_='main-content').find_all('div')
        for div in divlist:
            if div.get('class')==None:
                continue
            # print(div.get('class'))
            if 'para-title' in  div.get('class') and 'level-2' in  div.get('class'):
                ti_re=div.find('span',class_='title-prefix').get_text()
                title=div.find('h2',class_='title-text').get_text().replace(ti_re,'')
                n=n+1
                if n>len(row)-1:
                    row=row+['' for t in range(n-len(row)+1)]

                row[n]=row[n]+title+':'
                
            elif 'para-title' in  div.get('class') and 'level-2' not in  div.get('class'):
                if n>len(row)-1:
                    row=row+['' for t in range(n-len(row)+1)]
                row[n]=row[n]+div.get_text()+'\n'   
            elif 'para' in  div.get('class') and n!=-1:
                if n>len(row)-1:
                    row=row+['' for t in range(n-len(row)+1)]
                row[n]=row[n]+div.get_text()+'\n'

            else:
                pass
        for j in range(len(row)):
            sheet.write(r,j,row[j])
        r=r+1
        # break
    workbook.close()
# sort_out1()