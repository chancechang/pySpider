
from bs4 import BeautifulSoup
import requests
import xlsxwriter
import re





page=456
privince='19黑龙江1'
urlroot='http://218.7.20.115:9011/pub/GongShiSearch'

cook='security_session_verify=9a68bf68e6be9cb0a4c9340cd811c5d4; __RequestVerificationToken=; __RequestVerificationToken_Lw__=nIwvG3M9SnkXbU+nfQHhGA4heNkRCm6p/eukqQc0L+biDpIKpJsWt7A6/A8sVS2J+mb5SZ0Ci9crCI6YU3VEp3p2xXb8+zWzr8BtzmAmpIwl1D75uO8gkjOOfnBCmmRh5xh3Zkkrhpk6+IUwlJI7TSWpLpnsNUIMNn83e2piq90=; ASP.NET_SessionId=yqcg0heoey4zcjfuu1blfgqs'
cook='__RequestVerificationToken=; __RequestVerificationToken_Lw__=O8Hc4SRTqweLNOXjp+yE4NxQvJUXm7FYJT2869pM9NmyT1WKY6XijwjFX/p13x2n+GDM5Tkv4BN2Lkdj0Hh5GE6XVzGCvKbWaBWVVemZPNY4a/CKY4ZK6FpAXMj/wMHVVVT1L7C9pPZs0ASU84rvemjEWKrl6SK0ZkHvS99nx88=; ASP.NET_SessionId=ufpktvxbbu4l4bscyszltj01'
cook='__RequestVerificationToken=; __RequestVerificationToken_Lw__=FGIkd0kSZQIAfK4ytor8UoCe2C6140v+hbqJYOZkNEtxxww8nEnrbYVBJCgjQv08ukr3K0oVLDiFzCjRfyyhrm/zN3ih8IJQyH9+Ujqd+6WA2nesx8sUQ6rLjxrY9iEOs/oTv+bwAct7f1ur9WUk40MTj9QmhiYik8b/vjr/vA8=; ASP.NET_SessionId=hwc2yef33oheuehfrf04wmaj'
cook='__RequestVerificationToken=; __RequestVerificationToken_Lw__=KyuInWJ2h6I+WEu3chf5fYKZrNaerptfaOx2az4W9YMKHtT8Upm0wdkA5u3Xl7R1NJnYgl0SrOgcD//+aV566zPItrDR1dtTRXoTybNcwwW7+m5MW6d+QyVNzlI1zYNVw74mkTlaTrswGUiAbPYlgsmZdwcLFJH4cO8gVRGVUhA=; ASP.NET_SessionId=ibayxpy5ftxzfgqv5r2q0vvy'
cook='__RequestVerificationToken=; __RequestVerificationToken_Lw__=rW5JNzcgFVxgdFaPLTuW3WppDIUOfvqxeTo+LCT+4S2PxTA2Fcw6CUJViAAC4IAliIMFui9jZpGIiL5QZ6ngsxsmHoU46SaIt2XHWifyLItYWnVaaNDtHA7mnq01wW4PWCLnTn+4vCdC2Zd0KIY6Nfg/5bzLMHTVkPjhnjO2XTs=; ASP.NET_SessionId=llbioojmbskp2ndyawtbmlea'
dd='hCWkPEyiR/O0fw2jh4WR/iMXVifOzdM8HPdxXHo2jw/5gYp0M7zKnKBqdNd3YLpxS3N6jfMaB5zstcOvDBCVwRuEWWXqhJH19381qa1zRg3fq8MuadXCNoyHGA0F1NdK+OeSxp+mDeqlWwAPI0tD5RxyeIrmYrSJexcbUxep1L4='
dd='rHZ2JEPk6PlJZxsSxuh5nUTgRvt6YtFo8nONmY97SWTKxd7hzhCuinbkszPSz1PUHEzNcd3xv5jm8sANkTmMTtrgpskpI23qLYJLSGzJfJZIltmTf3E8KYu+qXZfi7OtmksdWwXScKEes5jhW0W+BNijJruXcyohYNH/xccLx8Q='
dd='7ikC62Fox9v4Xlyi4O0hJ1QR7PagQ/6FUL7tHxhF6nwiixmisrQ7hF87CcJw0o4upYYQOqRraOUdEqAhxMJrR9McMN3VOXbFiDF3cBBYPcz87LQZCCcUeLCH3AfY1b5SSq2yIN8SiUuxpby8On4MojKdjk3pKcwGXryMk3HrdiE='
dd='n2xDnl6wAqD3oMDRcl+x4nzkC44B0IbqWNOFDJ8KLONCLG+ATwiQhHu7ev/HIGLtlnWF+k5D4ddVt+AcikNadPnaQ0fRV6NroGFtfXu48/TpMF9eT9/4hp4fGJnyLv4yx2Uk4eTa4aHToWrDJQlJLFkpTfwpxKgKZeYRZz+dpfg='
dd='0uCx5DsDzbIwE4tvt0SP7mt8oaMcSofUOfkBjZ6+z5Mx/CHD1FsEdna6HhcXhpojnT0Y/18uiyOfXka27nzdNok5ylm4xoDpgdW++Ngizcd7EH/Zi7JPzlyC/XEtw+/xSAjqOz6G8tWb9wmo7Xb+b6XxNtCT1R/PQ/a3WPTCNTM='
header={
    'Cookie':cook,
}

data={
    '__RequestVerificationToken':dd,
    'p':'打（压）捆机'
}
def get_data():
    f=open(privince+'.txt','w+',encoding='utf-8')
    for i in range(240,page+1):
        print('第'+str(i)+'页')
        url=urlroot+'?pageIndex='+str(i)
        req=requests.post(url,data=data,headers=header)
        # url='http://2018.nmnjbt2015.com/pub/gongshi?pageIndex='+str(i)+'&p=%E6%89%93%EF%BC%88%E5%8E%8B%EF%BC%89%E6%8D%86%E6%9C%BA'
        # req=requests.get(url,headers=header)
        bsObj=BeautifulSoup(req.text,'html.parser')
        trlist=bsObj.find('tbody',{'id':'list-pub'}).find_all('tr')
        for tr in trlist:
            row=[]
            tdlist=tr.find_all('td')
            # print(len(tdlist))
            if len(tdlist)!=15:
                print('横向长度出现不为15的')
            for td in tdlist:
                row.append(td.get_text())
            f.write(str(row)+'\n')
        if len(trlist)<15:
            break
        # break
    # print(req.text)
    f.close()


def write_excel():
    workbook = xlsxwriter.Workbook(privince+ '农机购置补贴情况.xlsx') #创建工作簿
    sheet = workbook.add_worksheet()

    workformat = workbook.add_format({
    'bold':  True,                 #字体加粗
    })

    rowname=['序号','县','所在乡(镇)','所在村组','购机者姓名','机具品目','生产厂家','产品名称','购买机型','购买数量(台)','经销商','单台销售价格(元)','单台补贴额(元)','总补贴额(元)','状态',]
    for m in range(15):
            sheet.write(0,m,rowname[m],workformat)
    r=1
    for line in open(privince+'.txt','r',encoding='utf-8'):
        line=eval(line)
        for m in range(len(line)):
            sheet.write(r,m,line[m].replace('\r','').replace('\n','').replace('\t','').replace('\xa0','').strip())
        r=r+1
    workbook.close()

get_data()

# write_excel()