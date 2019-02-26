import json
import csv
f=open('gwqc.txt','r',encoding='gb18030')
data=json.loads(f.read())
f=open('gwqc.csv','w+',newline='')
csv_write=csv.writer(f)
for i in data:
    # print(i)
    csv_write.writerow([i['ID'],i['DealersID'],i['Address'],i['Brand'],i['ShopSaleTel']])
    