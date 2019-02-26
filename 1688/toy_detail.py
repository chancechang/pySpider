from bs4 import BeautifulSoup
import requests
import csv
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp

f=open('dmqxtoy_final.csv','w+',encoding='gb18030',newline='')
csv_write=csv.writer(f)
f_error=open('dmqxtoy_error.csv','w+',encoding='gb18030',newline='')
csv_write1=csv.writer(f_error)
def get_detail(line):
    bs_obj=mytemp.getObj(line[1],True)
    img_link=bs_obj.find('div',class_='tab-pane').find('img').attrs['src']
    weight=''
    try:
        weight_list=bs_obj.find('div',class_='attributes-item mod-info kuajing-attribues').find_all('span')
        for w in weight_list:
            weight_content=w.get_text()
            if weight_content.find('产品净重')!=-1:
                weight=weight_content.replace('产品净重','').replace('\n','')
                break 
    except:
        csv_write1.writerow(line)
        print(line)
          

    #寻找规格
    guige=''
    td_list=bs_obj.find('div',{'id':'mod-detail-attributes'}).find_all('td')
    for m in range(0,len(td_list)):
        # print(td_list[m].get_text())
        if td_list[m].get_text().find('规格')!=-1:
            guige=td_list[m+1].get_text()
            break
    row=line+[img_link,weight,guige]
    #价格和数量

    price_list=bs_obj.find('div',{'id':'mod-detail-price'})
    price_td_list=price_list.find('tr',class_='price').find_all('td')
    amount_td_list=price_list.find('tr',class_='amount').find_all('td')
    for n in range(1,len(price_td_list)):
        row.append(price_td_list[n].get_text()+' '+amount_td_list[n].get_text())

    print(row)
    csv_write.writerow(row)
    
r=0
for line in csv.reader(open('dmqxtoy_f.csv','r',encoding='gb18030')):
    print(r)
    r=r+1
    # line[1]='https://detail.1688.com/offer/571518606567.html?spm=a2615.7691456.newlist.120.1d534da3uiGZyp'
    get_detail(line)
    # break