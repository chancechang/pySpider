
import requests
import json
from bs4 import BeautifulSoup
import sys
import csv
sys.path.append("..")
import mytemp

def getBrand():
    url='https://car.m.autohome.com.cn'

    f1=open('car_autohome.txt','w+',encoding='utf-8')
    # csv_write1=csv.writer(f1)
    bsObj=mytemp.getObj(url)
    # f.write(str(bsObj))
    lilist=bsObj.find('div',{'id':'div_ListBrand'}).find_all('li')
    for li in lilist:
        brandCode=li.attrs['v']
        brand=li.find('span').get_text()
        f1.write(str([brand,brandCode])+'\n')

    f2=open('car_series.txt','w+',encoding='utf-8')
    for line in open('car_autohome.txt','r',encoding='utf-8'):
        line=eval(line)
        url='https://car.m.autohome.com.cn/ashx/GetSeriesByBrandId.ashx?r=6s&b='+str(line[1])
        js=json.loads(requests.get(url).text)
        # print(js)
        serieslist=js['result']['allSellSeries']
        if serieslist==[]:
            print('为空')
            break
        for se in serieslist:
            for s in se['SeriesItems']:
                row=[line[0],s['name'],s['id']]
                # print(row)
                f2.write(str(row)+'\n')





def main():
    f3=open('car_luntai.csv','a+',encoding='gb18030',newline='')
    csv_write=csv.writer(f3)
    # csv_write.writerow(['品牌','系列','车款','胎宽','扁平比','直径','胎宽','扁平比','直径'])
    for line in open('car_series.txt','r',encoding='utf-8'):
        line=eval(line)
        dic={}
        url='https://car.m.autohome.com.cn/ashx/car/GetModelConfigNew2.ashx?seriesId='+str(line[2])
        # url='https://car.m.autohome.com.cn/ashx/car/GetModelConfigNew2.ashx?seriesId='+'3909'
        # print(url)
        js=requests.get(url)    
        try:
            data=json.loads(json.loads(js.text)['data'])
        except:
            print(url)
            break
        param=data['param']
        for p in param:
            if p['name']=='基本参数':
                for pa in p['paramitems']:
                    if pa['name']=='车型名称':
                        for val in pa['valueitems']:
                            text=BeautifulSoup(val["value"],'html.parser').get_text()
                            dic[val["specid"]]=[text]
                        # break
            m=-1            
            if p['name']=='车轮制动':
                # print(len(p['paramitems']))
                # break
                for t in range(len(p['paramitems'])):
                    pa=p['paramitems'][t]
                    # print(BeautifulSoup(pa['name'],'html.parser'))
                    if BeautifulSoup(pa['name'],'html.parser').get_text()=='轮胎':
                        m=t
                if m!=-1:
                    for t in range(m,m+2):
                        pa=p['paramitems'][t]                
                        for val in pa['valueitems']:
                            # text=BeautifulSoup(val["value"],'html.parser').get_text()
                            text=val["value"].split(' ')
                            try:
                                text=text[0].split('/')+[text[1]]
                            except:
                                text=[text[0],text[0]]+[text[0]]
                            dic[val["specid"]]=dic[val["specid"]]+text
                    # break
        # print(dic)
        for key ,value in dic.items():
            row=line[:2]+value
            csv_write.writerow(row)
            print(row)
        # break
        
main()
