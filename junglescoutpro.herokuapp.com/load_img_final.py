import requests
import os
import csv
import time
import xlsxwriter

date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
root = "./"+date+"jungle_img/"
searchText = 'apple 8'
filename = date+'jungle_'+searchText.replace(' ', '_')+'.csv'

workbook = xlsxwriter.Workbook('./'+filename.replace('.csv', '.xlsx'))
worksheet = workbook.add_worksheet()
rol = 0

for line in csv.reader(open(filename, 'r', encoding='gb18030')):
    if line[17] == 'imageUrl' or line[17] == 'N.A.':
        cel = 0
        for item in line:
            worksheet.write(rol, cel, item)
            cel += 1
        worksheet.set_column(cel-1,cel,80)
        worksheet.set_row(rol, 50)
        rol += 1
        continue
    url = line[17]
    print(url)
    path = root + url.split("/")[-1]
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = requests.get(url)
            r.raise_for_status()
            # 使用with语句可以不用自己手动关闭已经打开的文件流
            with open(path, "wb") as f:  # 开始写文件，wb代表写二进制文件
                f.write(r.content)
            print("爬取完成")
        else:
            print("文件已存在")
    except Exception as e:
        print("爬取失败:"+str(e))

    cel = 0
    for item in line:
        worksheet.write(rol, cel, item)
        cel += 1
    worksheet.set_column(cel-1,cel,80)
    worksheet.insert_image(rol, cel, path)
    worksheet.set_row(rol, 50)
    rol += 1
workbook.close()
