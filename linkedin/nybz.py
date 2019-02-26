import requests
from bs4 import BeautifulSoup
import xlsxwriter
Page=286
filename='农业标准化信息'
# url='http://sfq.ahqi.gov.cn/demoQuery/list?pageNow=2&demoCode=&demoName=&assumeUnit=&cityId=0&productId=&demoBatch=&mgrMode=&demoLevel=&beginYear='
workbook = xlsxwriter.Workbook('./'+filename+'.xlsx')
worksheet = workbook.add_worksheet()
rol = 0
f_error=open('error.txt','w+')
cook='FSSBBIl1UgzbN7N80S=zbcsMeXw3NgTc5S1CThfbFMt3s6D8ompWALBVIHZyd4UYc7mAidwzQM8pwE1w5EY; JSESSIONID=8027CE7F7FFBC2EFB0DBD6AFA0FB76B3; FSSBBIl1UgzbN7N80T=1q8lBcuc7SG1gOuMcM_xYVGM26nC3nANxjTBb71fRBXm7wL3vZ83W0gOKhf5qnrt250Q1c6iGlB1FSjM4jHwgDC28UUsCJEzE_7iLGJ.BEZWlftJBxv2qd7uL4NvQpDZXIPePWex7wi_4wM0XQu3X33Tu9_nGsHMOMCwCn5kuHsltZ.wFA0i3XldWu7XlF.kZaIvNcNLzgMHXnyDTHNDYjANgwAVm9mQq9fplVja5KFGGUGr.LFAkjEr68tqLdBOST_GVnlnl9JQdNMeBEzysJhsPVKzbyNgeX3bJuqghYQf_5TAE3pRyQ1ojQneoLAvZccdVwrHgGGjbpJxTiVv8esY0'
cook='FSSBBIl1UgzbN7N80S=zbcsMeXw3NgTc5S1CThfbFMt3s6D8ompWALBVIHZyd4UYc7mAidwzQM8pwE1w5EY; JSESSIONID=A0CE6CAEC63E7D258A2F53C813993CE5; FSSBBIl1UgzbN7N80T=1ODnPf.0f1g9Tq.zHgPd36gzLVjqYpEIlxzR.HtUVWCuf5aXjIDXrUGYMLyEJpRZLw7jIfBgzv69U1nzCxU.T2XssJggHIbOtIRFW0H7aMOLSydLyhX_DrtOdVw3I1DbFlrpCv4KQpd_5IfSjOjxcSvtQDMVPdQG1s1jxc.XjgKwgwFbvgOB0QyYIuCqLoGserLAILhj1oyKLcxz4_o9nC97yBfxbZKEaGrWXnxe1wX9t5jM80wLbOrkYLU_V13B0ivsHhtWTo8f0k_jxpv9414SKaMWF1rMDDETWb8hXWVyjmfB7xz9.SojUeExJQbOvqDMdg7K2XvcKKP.aft1CGVgz'
header={
    'Cookie':cook,
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    'Upgrade-Insecure-Requests':"1",
    'Host':'sfq.ahqi.gov.cn',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Referer':'http://sfq.ahqi.gov.cn/demoQuery/list?pageNow=2&demoCode=&demoName=&assumeUnit=&cityId=0&productId=&demoBatch=&mgrMode=&demoLevel=&beginYear='
}
def main():
    for i in range(1,Page+1):
        url='http://sfq.ahqi.gov.cn/demoQuery/list?pageNow='+str(i)+'&demoCode=&demoName=&assumeUnit=&cityId=0&productId=&demoBatch=&mgrMode=&demoLevel=&beginYear='
        for j in range(5):
            try:
                html=requests.get(url)
                # html.encoding='utf-8'
                print(html)
                bsObj=BeautifulSoup(html.text,'html.parser')
                break
            except:
                time.sleep(3)
            if j==4:
                print('第'+str(i)+'页抓取失败')
                f_error.write(url+'\n')
        # print(bsObj)
        table=bsObj.find('div',class_='pro_body')
        trlist=table.find_all('tr')
        if i==1:
            thlist=table.find('theader').find_all('th')
            
            for th in thlist:
                worksheet.write(rol, cel, th.get_text())
                cel += 1
            rol=rol+1

        for tr in trlist:
            tdlist=tr.find_all('td')
            cel=0
            for td in tdlist:
                worksheet.write(rol, cel, td.get_text())
                cel += 1
            rol=rol+1
            
        
main()