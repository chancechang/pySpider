import requests
from bs4 import BeautifulSoup
import time
from email.mime.text import MIMEText
import smtplib #python 内置函数，无需安装

def getObj(url):
    for i in range(5):
        try:
            req=requests.get(url, headers=header, timeout=15)
            req.encoding='utf-8'
            # print(req.text)
            bsObj=BeautifulSoup(req.text,'html.parser')
            # print(bsObj)
            select=bsObj.find('select',{'id':'size'})
            if select!=None:
                return select
        except:
            time.sleep(3)
        if i==4:
            return None

def sendmsg(msg,from_addr,password,to_addr):
    # 输入SMTP服务器地址:
    smtp_server = 'smtp.qq.com'  #163邮箱为'smtp.163.com'
    server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

# from_addr = input('From: ')
# password = input('Password: ')
# to_addr = input('To: ')
# t=int(input('时间间隔（s）：'))
# cook=input('输入cookie:')


from_addr = '1643146364@qq.com'
password = 'woshige123'
to_addr = '1509662199@qq.com'
t=25
cook='locale=19e8b303dd0242e55dafdd2966d6af00172cce21076806dbb398293b6f73b1e2a%3A2%3A%7Bi%3A0%3Bs%3A6%3A%22locale%22%3Bi%3A1%3Bs%3A5%3A%22zh-CN%22%3B%7D; route=17f8595040b784d151dc6de42d37bd1e; mdnsonline=dnml3jsu850epsl7rgv98c3ku0; _csrf-frontend=606c7ccd3c0cc992e5d58115645161a01fc424640633e8e7573c1254871b203ea%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%227SvqHrvsuyubKjjoOQlYs5ZOLghXenAS%22%3B%7D; _gat=1; _ga=GA1.2.394791729.1544238888; _gid=GA1.2.1714988061.1544238888; __atuvc=10%7C49; __atuvs=5c0b4544a8114eca003'
header={
    'Cookie':cook,
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
}


# idlist=[1710,1702,1703,1704,1705,1711,1610,1662]
idlist=[1727,1728,1711]
# last=[False,False,False,False,False,False,False,False]

while True:
    for i in range(len(idlist)):
        url='https://www.mdnsonline.com/product/'+str(idlist[i])
        print('正在检查'+url)
        select=getObj(url)
        # print(select.get_text())
        # continue
        if select==None:
            print('请求失败，请检查是否登录失效')
            continue
        m=len(select.find_all('option'))
        selText=select.get_text()
        if 'SIZE' in selText:
            n=selText.count('OUT')        
        else:
            n=selText.count('沽清')
            
        # print(m,n)
        if m-1>n:
            # 发送邮件
            print('有货,即将发送邮件')
            msg = MIMEText(url, 'plain', 'utf-8')
            sendmsg(msg,from_addr,password,to_addr)
        else:
            print('无货')
        time.sleep(t)
    # break


