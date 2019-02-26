import re
import sys
sys.path.append("..")
import mytemp
import requests
import json
import xlsxwriter


cook='_gcl_au=1.1.406759832.1540991883; SPC_IA=-1; SPC_EC=-; SPC_U=-; SPC_F=sZZK1WAOWYh2digKb5OgzNqzY1yZeSpi; REC_T_ID=698b2d0c-dd0f-11e8-9371-5254000ba6e2; SPC_T_ID="itP5E75zMS1Vcj4vBmLdPsfGDyups0vVRlBKh437g1dW2pxIkXztUVYTJaQfUHsbXot0TOrUAdGmlfNJL3W2i+rTJjIQ57eadx2v4re6kHc="; SPC_T_IV="JgQLS5+XOJaQaXZUvmthCA=="; _ga=GA1.3.173483500.1540991913; SPC_SI=d45k1aivr7df43iata6vtfhznxmb55dg; _gid=GA1.3.676164037.1541241178; csrftoken=PvkiumpY4S26L7st13R5an13jk8GMKES'

header={
    'Cookie':cook,
    'x-api-source':'pc',
    'x-requested-with':'XMLHttpRequest',
    'if-none-match-':'55b03-25ed7b0b9627c4a6413e2ed43f996549',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    # 'referer':'https://shopee.co.id/Handphone-Tablet-cat.40.1211?page=2&sortBy=pop'
}
def get_json(url):
    for i in range(5):
        try:
            bsObj=requests.get(url,headers=header,timeout=10)
            js=json.loads(bsObj.text)
            return js
        except:
            pass
    return None
def get_class(itemid,shopid):
    url='https://shopee.co.id/api/v2/item/get?itemid='+str(itemid)+'&shopid='+str(shopid)
    js=get_json(url)['item']
    categories=js['categories']
    display=''
    for cate in categories:
        display_name=cate['display_name']
        if display_name==None:
            continue
        display=display+display_name+'>'
    sold=js['sold']
    # 店铺名
    return [display,sold]
# get_class()
def get_shopname(itemid,shopid):
    # url='https://shopee.co.id/api/v0/shop/'+str(shopid)+'/item/'+str(itemid)+'/shipping_fee/'
    url='https://shopee.co.id/api/v2/shop/get?is_brief=1&shopid='+str(shopid)
    try:
        js=get_json(url)['data']['account']['username']
    except:
        js=''
    return js
#Bluetooth
def get_name(id):
    # url='https://shopee.co.id/Bluetooth-Headset-cat.40.1205'
    # id=1205
    for i in range(100):
        url='https://shopee.co.id/api/v2/search_items/?by=pop&limit=50&match_id='+str(id)+'&newest='+str(i*50)+'&order=desc&page_type=search'
        js=get_json(url)['items']
        if js==None:
            raise EOFError
        for item in js:
            itemid=item['itemid']
            shopid=item['shopid']
            itemName=item['name']
            # sold=item['sold']
            class_sold=get_class(itemid,shopid)
            row=[itemid,shopid,itemName]+[class_sold[0]+itemName,class_sold[1]]+[get_shopname(itemid,shopid)]
            # row=[itemid,shopid,itemName,sold]
            # print(row)
            f.write(str(row)+'\n')
def main():            
    idlist=[1205,1187,1185,1201,10391,18000,1207,1203,12652,1189,2837]
    f=open('shopie.txt','a+',encoding='utf-8')
    for id in idlist:
        print(id)
        get_name(id)
    f.close()

workbook=xlsxwriter.Workbook('shopie.xlsx')
sheet1=workbook.add_worksheet()
i=0
for line in open('shopie.txt','r',encoding='utf-8'):
    line=eval(line)
    # print(len(line))
    # break
    titlelink=line[2].replace('+',' ').replace('/',' ').replace('|',' ').replace(',',' ').replace('[',' ').replace(']',' ').replace('?',' ').replace('-',' ')+' '
    titlelink=re.sub(' +',' ',titlelink)
    titlelink=titlelink.replace(' ','-')
    link='https://shopee.co.id/'+titlelink+'i.'+str(line[1])+'.'+str(line[0])
    line=[link]+line
    for j in range(7):
        sheet1.write(i,j,line[j])
    i=i+1
workbook.close()