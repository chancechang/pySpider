
import requests
import csv
import time
import json
import re

#可修改商品链接,必须保证是天猫商品，商品链接以https://detail.tmall.com/item.htm?开头
url='https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-14719154061.57.782d4cdbP8fb28&id=535690525088&rn=6fe7286c001ddefcb7acc9fbfe76f709&abbucket=20'
# url='https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.c8ef47e0rWInGp&id=533686170835&skuId=3485403728929&areaId=420100&user_id=2784810953&cat_id=50068008&is_b=1&rn=47b205f5d4aecfbf8ed9e28b1186a7f1'
filename='雅诗'
MAX_page=100
itemId=563310634
# itemId=re.search(r'&id=(.+?)&',url).group(1)
# sellerId=re.search(r'&user_id=(.+?)&',url).group(1)

header={
    'Cookie':'cna=h9/yEVZzcBsCAXrNB8OEFnAP; hng=CN%7Czh-CN%7CCNY%7C156; t=8464a4877acc365c142612d5c3535d73; _tb_token_=e358e1f3ded84; cookie2=19ae29c470f405b80275dd52baefe35c; _m_h5_tk=64705fff8ba6e9dd50853f5f5b9929cb_1539873398765; _m_h5_tk_enc=5301f3c7015e41bb1026840101c64f24; isg=BLa2zIBT8ckLPYVntQfzqzz5B-yy2bKuS2z84iCeMxlZY1L9iGQwIXVVf3-qS_Ip'
# referer:https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-14466283798.50.43547440H0DfBt&id=40545566432&rn=6fe19d846dcf80351798b26fa5bfdf95&abbucket=20&skuId=3854687709703'
}

f1=open(filename+'.csv','w+',encoding='gb18030',newline='')
csv_write=csv.writer(f1)
def main():
    lastText=''
    for i in range(1,MAX_page):
        print('开始爬取第'+str(i)+'页')
        url='https://rate.tmall.com/list_detail_rate.htm?itemId='+str(itemId)+'&sellerId='+str()+'&order=3&currentPage='+str(i)
        url='https://rate.tmall.com/list_detail_rate.htm?itemId=535690525088&sellerId=1790973264&order=3&currentPage=3'
        er=False
        for j in range(0,5):       
            bsObj=requests.get(url,headers=header)
            tx=bsObj.text.strip()
            start=tx.find('(')+1
            jstext=tx[start:].replace(')','')
            try:
                ratelist=json.loads(jstext)['rateDetail']['rateList']
                break
            except:
                time.sleep(5)
                continue
            if j==4:
                er=True
        print(ratelist)
        # break
        if er==True:
            print('第'+str(i)+'页跳过')
            continue
        for rate in ratelist:
            rateCon=rate['rateContent']
            #若不需要追评，可注释掉下面这一行
            if rate['appendComment']!=None:
                rateCon=rateCon+rate['appendComment']["content"]
            print(rateCon)
            csv_write.writerow([rateCon])
            
main()