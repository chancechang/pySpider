from bs4 import BeautifulSoup
import requests
from urllib.error import HTTPError
import time
from email.mime.text import MIMEText
import smtplib #python 内置函数，无需安装
import urllib3

#必看：
    #除import提到的包外，还需要安装的包
    # pip install pyopenssl
    # pip install ndg-httpsclient
    # pip install pyasn1
    #setmsg函数中补充发件邮箱和密码信息以及收件邮箱信息

cook="AKA_A2=A; akaas_AS_CA=2147483647~rv=36~id=7b1cd9906c25e2b9921a215064e74665; _abck=6B7A81BDE3A9C62647BCEF4C2F608948CFE2714D24700000B481A45B16D5B238~-1~vS+b0FVki0n8eXxlqKhWjvNUHW8upaX4KLlt9Wt2lDY=~-1~-1; bm_sz=4A4FE015930AE871B27A8CB3D0DC8AF9~QAAQTXHiz3qAZOplAQAANaqa+sNrLwxFN4RifkuyAFPhoJImDqgd5SbQ0O/n/fSa8Cb2PL0iMIweZYY7Ity+ZTfuKQBhF7vt/6Yb5ZR3ijobT354Tr1KZVmltKR92ZSeybwNphRnFIsR4gvprwIZJGQxo3nh6WOP+tiVTvMjBh452Xd7Slhy7+bJ6P7u; check=true; AMCVS_97B21CFE5329614E0A490D45%40AdobeOrg=1; AMCV_97B21CFE5329614E0A490D45%40AdobeOrg=-330454231%7CMCIDTS%7C17796%7CMCMID%7C62350747535273031870287669242920445768%7CMCAAMLH-1538112567%7C9%7CMCAAMB-1538112567%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1537514967s%7CNONE%7CvVersion%7C3.1.2; s_cc=true; CRTOABE=0; ak_bmsc=CAF07F25E40A8F696497B5B8B5DB8B4CCFE2714D24700000B481A45B38376045~pl600+C8HPl6yWLVqueQvtcKiqoBAkfUKOGqdslwge/U3qh1UDNueDEL2SsxenvDhzbjt5zWUEClytAPcw+h8q1y6lDrQULEu0kIbeulcmahUgBAGMNTNn1ZH0FU/KHHpohZ9eSssBzSuNVintSTWugVl73Spg94NLWvfJSvryhueuBZee8VPkVPZH6Sy8hXHqsD6IwdKE+tN0jf3awgRPFkuiaDaSInuqUZmEfAhZLZFUvQQWZaTefj0ozdn9+y3D; WRUID20171123=1924093959766611; BVImplnative_review_form=20040_1_0; spid=ABD939D6-F356-491A-821F-D7617338E8CF; sp_ssid=1537507777847; BVBRANDID=1e95c795-552e-458d-bb0a-f9a3ca556a59; BVBRANDSID=b9504abe-17fb-42e0-a323-6bbdf7c5f36d; JSESSIONID=0000qdukakIbAYRI3tNQ3mIinuf:163c2ees7; WC_SESSION_ESTABLISHED=true; WC_PERSISTENT=dNnGQ1r06GR%2Bu5r%2FM7Z%2FnDDpUhQ%3D%0A%3B2018-09-20+22%3A30%3A17.098_1537507817096-77013_10302_-1002%2C-24%2CCAD%2CjPk%2BTNMAc4rqoc89xgCzLp02PM7FeGCovimAoinWmSFdYrMWgf8535%2Fx3GlbJV6escHGzmkZ6oFDLeWpYbLrIA%3D%3D_10302; WC_AUTHENTICATION_-1002=-1002%2C5M9R2fZEDWOZ1d8MBwy40LOFIV0%3D; WC_ACTIVEPOINTER=-24%2C10302; WC_USERACTIVITY_-1002=-1002%2C10302%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2CkKMlcCtoJEP%2Bj9bJjSGPFGugv3rA4J%2BzUBHYySw3VMfrQBy2eiimhZQ%2FTNuM%2BAqQcKifgb1rVecL7luknzCf8amwHeEUfAJvwSNoO%2F5jrR77VCgS%2BmS6a5ebncjN4MHrVpn3Hy7T4m%2FmhlFlIEc51eKSDzOicU5E0wi6hljyclHZ%2B0Bl%2F3foMdcGpB7C8WI8Kv4eIZdtiOjoE94l4kUv7g%3D%3D; WC_GENERIC_ACTIVITYDATA=[7522564441%3Atrue%3Afalse%3A0%3AT%2BW69MSk0L7vnquXgj7XC8ou7Go%3D][com.ibm.commerce.context.audit.AuditContext|1537507817096-77013][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][CTXSETNAME|Store][com.ibm.commerce.context.globalization.GlobalizationContext|-24%26CAD%26-24%26CAD][com.ibm.commerce.catalog.businesscontext.CatalogContext|11201%26null%26false%26false%26false][com.ibm.commerce.context.ExternalCartContext|null][com.ibm.commerce.context.base.BaseContext|10302%26-1002%26-1002%26-1][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.context.entitlement.EntitlementContext|4000000000000001004%264000000000000001004%26null%26-2000%26null%26null%26null][com.ibm.commerce.giftcenter.context.GiftCenterContext|null%26null%26null]; C_CLIENT_SESSION_ID=1d8430e5-6ed1-4c22-90fe-1970ecac7f12; hl_p=1df1ead2-4347-4571-84cd-254c86d45791; C_LOC=CAAB; C_2LOC=false; s_sq=%5B%5BB%5D%5D; bm_sv=B477B80EE15212FFB9049929ACF0D205~D8dzhv9NU+NTSo7YMFXAzfDLoAMTUlRrBpznYUFEdNNXpJUWr14ro9lRrR6aaqlo9j1vIimS/Kmv08R72A1rGkjrliJYI/SRBhDOvUtyn1cFBkXeWwZaR99k7DnDddbeBMPwpSoTwrJqA9amjeI1S3+IbnVlZJcX6aiSmvuHiJU=; mbox=session#458bd7a27abd4c068925623dcc0a715d#1537510111|PC#458bd7a27abd4c068925623dcc0a715d.28_61#1600752569; __CT_Data=gpv=12&ckp=tld&dm=costco.ca&apv_81_www33=12&cpv_81_www33=12&rpv_81_www33=11; ctm={'pgv':2138690657458712|'vst':3070183073991961|'vstr':331026244913032|'intr':1537508317727|'v':1}"

header={
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9",
    "cache-control":"max-age=0",
    "cookie":cook,
    "upgrade-insecure-requests":"1",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
}
def getObj(url,encode='utf-8'):
    for i in range(1):
        try:
            urllib3.disable_warnings()
            html=requests.get(url,headers=header,verify=False)
            html.encoding=encode  
            break
        except HTTPError as e:
            # time.sleep(3)
            print('再次请求')
            print('HTTPError')
            return None
    try:
        bsObj = BeautifulSoup(html.text,'html.parser')
    except AttributeError as e:
        return None
    return bsObj
def sendmsg(msg):
    # 发件人Email地址和密码:
    from_addr = '1509662199@qq.com'  
    password = '' 
    # 输入SMTP服务器地址:
    smtp_server = 'smtp.qq.com'  #163邮箱为'smtp.163.com'
    # 收件人地址:
    to_addr = '1509662199@qq.com'         
    server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def main():
    url='https://www.costco.ca/Elizabeth-Arden-Ceramide-Advanced-Time-Complex-Capsules.product.100296958.html'
    #默认当前状态为无货
    now=False
    while True:   
        bsObj=getObj(url)
        try:
            if bsObj.find('div',{'id':'ctas'}).find('input',{'id':'add-to-cart-btn'}).attrs['value']=='Out of Stock':
                #缺货
                if now==True:#判断上个状态是否有货
                    #上个状态有货，发送缺货提醒
                    msg = MIMEText('缺货', 'plain', 'utf-8')
                    sendmsg(msg)
                    #修改状态
                    now=False         
            else:
                if now==False:#判断上个状态是否有货
                    #上个状态无货，发送有货提醒
                    msg = MIMEText('有货', 'plain', 'utf-8')
                    sendmsg(msg)
                    #修改状态
                    now=True 
        except:
            print('AttributeError')
        #隔多久查看一次，秒为单位
        time.sleep(10)
main()
