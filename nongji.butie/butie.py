
from bs4 import BeautifulSoup
import requests
import xlsxwriter
import re



page=1
privince='24—2018贵州'
urlroot='http://42.123.116.194:2018/pub/GongShiSearch'

cook='__RequestVerificationToken=; __RequestVerificationToken_Lw__=4EDW+mpynwTkqW3DETpxdWrxn5W8nj6kMXUofKCESrXXkSYTWX4iH7MuETUbxuum0oVst5OqG1adH3bD5CcZHbYB/Wi/nKWUpPe6aKuBOPQ9QUbdZJ+YGMdsYzv4so8C9APWkGQV8G1anChDbon7Gc/mgNG6PDcIVRMAd79hLPg=; ASP.NET_SessionId=3xallifuxjx0o4d34efwznwj'
cook='__RequestVerificationToken=; CKIE_AD_ANGE='
cook='__RequestVerificationToken=; __RequestVerificationToken_Lw__=uRfLp6zXal8K5svC6Zb8Mk3PotbCpEBEFD5xGm1EI55GHX68qe6VuQFeAuvASf7kKziRGOtmkK2Ev5XXoDnq2lYshz3wG05ctht4VIklXNZsrXViYmEYD1D8K2M600ieJ0mMhMyR1q6Y2ssS+y09LoDppN0KPkAUO1ezlvQRwfQ=; ASP.NET_SessionId=dyttcvze43vdd2m2p1q1ryyd'
cook='__RequestVerificationToken=; __RequestVerificationToken_Lw__=0li8GqdNBbj99TkBOGFmc/NP689MdanQzlr8yzlQLHNPYII62fG0WnVgKBYgPORgmnlJoHAptsPr0lsxz4PL8UWIpMGnVRz4Q1xIUyDZUws=; ASP.NET_SessionId=tr0ojn53yiqvmqr5fdmyssq2'
cook='__RequestVerificationToken=; __RequestVerificationToken_Lw__=o5Oz0h/kOjKi+0fXZb0KoTVtoo9vLtZ12f/hlMH1RQ35lIfTB23zLFjgEHPUAkcYo0gXAyM70nYf6DeubJ5U6y6+MU+fWMpaFwdnwrAMK0M16lwVrdhHT5p2l/V7WZRQl6ErSzD28JtXzIQsyVl9TgpFSAi6VDT4KdRyWlkZyaY=; ASP.NET_SessionId=yumlzhdwuqrv3cvvcuju3sqs'
cook='__RequestVerificationToken=; __RequestVerificationToken_Lw__=GI5Wx30ITZoWAFvppiQP6me19oHtrRHrsGvsrGQeuxB6LHqRTxm2oAIg3y7DJY40TjJ4L3r+F8+iL0o7XAqcnQVqS0NlZj8526g2bm0kCxE=; ASP.NET_SessionId=kkrcbzpg1e11jlhm2w4rqw2q'
cook='__RequestVerificationToken=; __RequestVerificationToken_Lw__=hy/7LNuj4UtDXXhfLf3YB7ga+rIymn3gM3jUVh8WOpPUX0L0+jDnKfawLt/3Q5R7cUSWmVci5bhUUwutJJxusnI7CzKOFcZo4uU9DwvM23vJgKt0qQixuhBxiazbxsD5QIRUAM0XpglLULPfSweJ6iMqoE/Ol+Gj32qZ4INfn4o=; ASP.NET_SessionId=sy4ywb3cfv24jeevocoqlk3d'
cook='__RequestVerificationToken=; __RequestVerificationToken_Lw__=XEggxNSMn0cnj5Cwt2CGogB3NsXuj41CXWS9JpU8bMmuCQM7Wn/MOUZ0Z/lXzJacCQNTNXn6msi+5YLAHYQHeqiiKtEWz4WbboDC87SigHEaawoUHpNX42E/R4C2hKiMHilOw/4RvgIBc/+KK2eGHsFVZmniP2QlO92hzeNsTqc=; ASP.NET_SessionId=j2ngotcchiw5pewrts4wddrr'
cook='__RequestVerificationToken=; __RequestVerificationToken_Lw__=9Ae8N4gk5hb/D9OP1XFV3LLuczB18HfN65CHTkS8NcpIvVmqt2EQQDoshIBb7qnXE7d8b6ckwj6vZR97RMr97EEccqOOOE6RrROlMuUZX6JD1yavMQhbPomxS98oN7Kk/FFj5LmZGQX9sA3En9XVLGSeP0NgdNbyMjDc7uDBz0Q=; ASP.NET_SessionId=elpsy3ceudb4selwb4tc3kax'
cook='__RequestVerificationToken=; __RequestVerificationToken_Lw__=TgBnp0Pm4ayj1m41TasGQjx88hyuDKOyxujfhh6p7PkDjaXoz9eSzZfWnrFvbmaDXjkbQH1rMOJg6HYEhIeFwPIs7jPOhL+qzHyuOdlzIko=; ASP.NET_SessionId=womlosyf21h4sr4cam1qnxg4'
dd='m+S6hUGtlQn2i+RhVMHrF2Am0045wGbq0cTIZLnTxHRD58cFn009D35pmOnJ8s2D2WwJs/cgQGdOX7soZYorHKQDQcEdOlCSZvmbbvHJbEVwzCbJVXC+Dw+LF6blmD84kkgr2189J4cuydeQR4vb/o0xtJFqrggQ0v0CMruTGKA='

dd='smp+Z9iBFiJhBKEg+6Wx90gDDSoIvbw8hcs3OM9aQMKwv6HpwvTjvRGNlS1c2VaDlSyssxvY70AlcqCXlzcZI6yv0J/tBMtw+z6ju0t5XPQL4+khioi7XDe3f+ce38ciEWid8PWb/IKv0w8ZwsoG0vYgpaxgVKPvzyR4iNJN/+w='
dd='GI5Wx30ITZoWAFvppiQP6me19oHtrRHrsGvsrGQeuxB6LHqRTxm2oAIg3y7DJY40TjJ4L3r+F8+iL0o7XAqcnQVqS0NlZj8526g2bm0kCxE='
dd='__RequestVerificationToken=; __RequestVerificationToken_Lw__=hy/7LNuj4UtDXXhfLf3YB7ga+rIymn3gM3jUVh8WOpPUX0L0+jDnKfawLt/3Q5R7cUSWmVci5bhUUwutJJxusnI7CzKOFcZo4uU9DwvM23vJgKt0qQixuhBxiazbxsD5QIRUAM0XpglLULPfSweJ6iMqoE/Ol+Gj32qZ4INfn4o=; ASP.NET_SessionId=sy4ywb3cfv24jeevocoqlk3d'
dd='2ilXMuiqBPbC/3uI3319qfem3wBe9c4CXazYqZRSe0cb81oCbHxVA7LMLte0NiSZOeX/2Ef7kKb6pFxBpU/aWvHCxxALtikFJMPzH+1uua51bQFFxtrdNWqClde3P0ee9877W77TpLmZU9x4URWLIklTgU5PRsQbEmExWooFFgc='
dd='vsbUkDAgfBeSlmRlWnCb5Lo+Kwrp4OxXD3QwzPhgP066rBHaEcZ/ZqtiHcNBM9wF5gY63QSPfJowZ1iPon89ypn38mnGzQFzPhApAaDlklSA1dsYsivtPUFiTalNrtIVGj9p32NdKuYvdZn9SIX1ht6uL7LyB++E/BG9qD2pY8E='
dd='+2fNX36u48FHhMF+32ie1fZ0pkRdL4VEBp+TvWQQ/z28Q4EUF4sJnMpB1ljHglw22xPQt64ECxyjaX/4t/Z93fb22qSjmvTqlooBlk4bIAA8rJuolwq9BkHdEpkmmkJKMmlZ7/RGa4xR7xLsJo0yf5FyWPIwuHeTlLOX/JWej2g='
dd='TgBnp0Pm4ayj1m41TasGQjx88hyuDKOyxujfhh6p7PkDjaXoz9eSzZfWnrFvbmaDXjkbQH1rMOJg6HYEhIeFwPIs7jPOhL+qzHyuOdlzIko='
header={
    'Cookie':cook,
}

data={
    '__RequestVerificationToken':dd,
    'p':'打（压）捆机'
}
def get_data():
    f=open(privince+'.txt','w+',encoding='utf-8')
    for i in range(1,page+1):
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

write_excel()