import xlrd
import os
import requests

cook='g=53965_1540194021620; g=HDF.23.5bcd8428412dd; newaskindex=1; CNZZDATA-FE=CNZZDATA-FE'
header={
    'Cookie':cook,
#     Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
# Accept-Encoding:gzip, deflate, br
# Accept-Language:zh-CN,zh;q=0.9
# Cache-Control:max-age=0
# Connection:keep-alive
    'Host':'www.haodf.com',
    'Referer':'https://www.haodf.com/',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}
def get_proxies_abuyun():
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"
    # 代理隧道验证信息
    proxyUser = 'HR3LY43V4QOU249D'
    proxyPass = 'F89DAEA7A6C85E23'

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies

def getImg(row):
    url=row[1].split('?')[0]
    name=row[0]
    hospi=row[2]
    keshi=row[3]
    # print(url)
    #医院科室姓名
    path=root+hospi+'_'+keshi+'_'+name+'.jpg'
    # path=root+'asds.jpg'
    # print(path)
    # return
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = requests.get(url,proxies=get_proxies_abuyun(), headers=header,timeout=15)
            r.raise_for_status()
            if r.content=="b''":
                print("爬取失败:"+str(e))
                return
            # print(r.content)
            # 使用with语句可以不用自己手动关闭已经打开的文件流
            with open(path, "wb") as f:  # 开始写文件，wb代表写二进制文件
                f.write(r.content)
            print("爬取完成")
        else:
            print("文件已存在")
    except Exception as e:
        print("爬取失败:"+str(e))


file='安贞医院'
data = xlrd.open_workbook(file+'.xlsx')
root='./'+file+'/'
# 通过索引获取工作表
sheet1 = data.sheets()[0]
# 通过名称获取工作表
sheet1 = data.sheet_by_name(u'安贞医院')
# 获取table对象，根据table进行该工作表相关数据的读取
# 获取行列
row = sheet1.nrows
col = sheet1.ncols
# print(row)
# print(col)

for r in range(1,row+1):
    rowlist=[]
    for i in range(1,5):
        cell_value=sheet1.cell(r, i).value
        rowlist.append(cell_value)
        # print(cell_value)
    if rowlist[1][:4]=='http':
        # print(rowlist)
        getImg(rowlist)
        # break
    # break
        


