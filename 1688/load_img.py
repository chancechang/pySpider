import requests
import os
import csv
# url = "https://ss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/logo/bd_logo1_31bdc765.png"
root = ".//dmqxtoy//"

# f=open('dmqxtoy_error_img.csv','w+',encoding='gb18030',newline='')
# csv_write=csv.writer(f)

for line in csv.reader(open('dmqxtoy_final.csv','r',encoding='gb18030')):  
    url=line[2]
    # print(url)
    path = root + url.split("/")[-1]
    # path = root + line[0].replace('/','').replace('*','').replace('?','').replace('\\','')+'.jpg'
    # .replace('/','').replace('*','').replace('\\','').replace('"','')
    print(path)
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = requests.get(url)
            r.raise_for_status()
            #使用with语句可以不用自己手动关闭已经打开的文件流
            with open(path,"wb") as f: #开始写文件，wb代表写二进制文件
                f.write(r.content)
            print("爬取完成")
        else:
            print("文件已存在")
    except Exception as e:
        print("爬取失败:"+str(e))
        # break
        # csv_write.writerow(line)

    
