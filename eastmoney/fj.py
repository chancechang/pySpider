from bs4 import BeautifulSoup
import requests
import csv
import sys
sys.path.append("..")
import mytemp

def main(url):
    targetdata=[]
    bsobj=mytemp.postObj(url,{})
    obj=bsobj.find('table',{'id':'ctl00_ContentPlaceHolder_gvList'}).findAll('tr')
    for j in range(1,len(obj)):
        a=obj[j].findAll('td')[1].find('a')
        href=a['href']
        name=a.get_text()
        tp=obj[j].findAll('td')[2].get_text()
        targetdata.append([name,href,tp])

    for i in range(5):
        data={}
        data['__VIEWSTATE']=bsobj.find('input',{'id':'__VIEWSTATE'})['value']
        data['__VIEWSTATEGENERATOR']=bsobj.find('input',{'id':'__VIEWSTATEGENERATOR'})['value']
        data['__EVENTVALIDATION']=bsobj.find('input',{'id':'__EVENTVALIDATION'})['value']
        data['ctl00$ContentPlaceHolder$rbtnSorce']=1
        data['__EVENTTARGET']='ctl00$ContentPlaceHolder$pGrid$nextpagebtn'
        bsobj=mytemp.postObj(url,data)
        obj=bsobj.find('table',{'id':'ctl00_ContentPlaceHolder_gvList'}).find_all('tr')
        for j in range(1,len(obj)):
            a=obj[j].findAll('td')[1].find('a')
            href=a['href']
            name=a.get_text()
            tp=obj[j].findAll('td')[2].get_text()
            targetdata.append([name,href,tp])
    return targetdata
url='http://www.fjjs.gov.cn:96/ConstructionInfoPublish/Pages/Projects.aspx'
# targetdata=main(url)


def crawl(driver):
    targetdata=[]
    for i in range(4):
        pageSource=driver.page_source
        bsObj=BeautifulSoup(pageSource,"html.parser")
        obj=bsObj.find('table',{'id':'ctl00_ContentPlaceHolder_gvList'}).findAll('tr')
        for j in range(1,len(obj)):
            a=obj[j].findAll('td')[1].find('a')
            href=a['href']
            name=a.get_text()
            tp=obj[j].findAll('td')[2].get_text()

            targetdata.append([name,href,tp])
        dl=driver.find_element_by_id("ctl00_ContentPlaceHolder_pGrid_nextpagebtn")
        dl.click()
    return targetdata

targetdata=mytemp.phangetObj(url,crawl)

mytemp.writetoCsv('blxt.csv',targetdata)
