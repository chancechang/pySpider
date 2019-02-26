
import requests
from bs4 import BeautifulSoup
import csv
import time

cook='f=n; id58=c5/njVq16t5zPL/cCrAbAg==; 58tj_uuid=0cdbf859-25a1-4c77-9c49-f4fa87562856; new_uv=1; utm_source=; spm=; init_refer=; commontopbar_new_city_info=79%7C%E6%9D%AD%E5%B7%9E%7Chz; commontopbar_ipcity=wh%7C%E6%AD%A6%E6%B1%89%7C0; als=0; commontopbar_myfeet_tooltip=end; xxzl_deviceid=FhVJ4gH32EG4Mr7184Y%2Fvjc4ACG0OHIN1tuTZlSXkerS6fnNB%2FZl5B0QWa8ujMu8; f=n; new_session=0; ppStore_fingerprint=D8B64B73082DA1C22E985E62866FE026BCF139877332963A%EF%BC%BF1521871946346'
headers = {
    "Cookie":cook,
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}


def getObj(url):
    req=None
    for i in range(5):
        try:
            req=requests.get(url,headers=headers,timeout=1000)
            req.encoding="utf-8"
            if req:
                break
        except:
            continue

    try:
        bsObj = BeautifulSoup(req.text,'html.parser')
    except AttributeError as e:
        return None
    return bsObj



def detailcrawl(url,title,csv_write,headlist):
    '''爬取详细信息，写到文件中
    '''
    bsObj=getObj(url)
    try:
        general=bsObj.find("div",{"id":"generalSituation"}).find_all("li")
        expense=bsObj.find("div",{"id":"generalExpense"}).find_all("li")
    except:
        return("error")
    index=["" for i in range(20)]
    index[0]=title
    index[1]=url
    for i in range(len(general)):
        text=general[i].find_all("span")[0].get_text()
        try:
            t=headlist.index(text)
        except:
            headlist.append(text)
            t=headlist.index(text)
        index[t]=general[i].find_all("span")[1].get_text()
    for i in range(len(expense)):
        text=expense[i].find_all("span")[0].get_text()
        try:
            t=headlist.index(text)
        except:
            headlist.append(text)
            t=headlist.index(text)
        index[t]=expense[i].find_all("span")[1].get_text()
    csv_write.writerow(index)


def crawl(url,f,page=1,n=0,sum=1110):
    '''爬取房屋链接，并存储
    '''
    if page==1:
        newurl=url
    else:
        newurl=url+"pn"+str(page)
    bsObj=getObj(newurl)
    try:
        divlists=bsObj.find_all("div",class_="list-info")
    except:
        print(url+"链接不可用")
        page+=1
        print("即将爬取链接为"+url+"的第"+str(page)+"页")
        return crawl(url,f,page=page,n=n)
    for div in divlists:
        a=div.find("h2",class_="title").find("a")
        title=a.get_text()
        href=a.attrs["href"]
        # print(title)
        if n<sum:
            f.write(str([title,href])+"\n")
            n+=1
        else:
            return
    page+=1
    print("即将爬取链接为"+url+"的第"+str(page)+"页")
    return crawl(url,f,page=page,n=n)


def getlinks(filename):
    '''从txt文件中读取链接
    '''
    links=[]
    f=open(filename,encoding="utf-8")
    link=f.readline()
    while link:
        links.append(link.strip())
        link=f.readline()
    return links


def main(filename):
    links=getlinks(filename)
    for i in range(len(links)):
        url=links[i].split("?")[0]
        print("开始爬取链接为 "+links[i]+"的网页,将房屋链接写入txt文件")
        detailinkfilename="./data/houselinks.txt"
        f=open(detailinkfilename,"w" ,encoding="utf-8")
        crawl(url,f)

        print(links[i]+"中房屋链接写入完毕，即将对房屋详细信息进行爬取")
        headlist=["标题","链接","房屋总价","房屋户型","房本面积","房屋朝向","所在楼层","装修情况","产权年限","建筑年代","房屋类型","交易权属","参考首付"]
        out=open("./data/hzhouse"+str(i+1)+".csv", 'w+',encoding='gb18030',newline = '')
        csv_write=csv.writer(out)
        
        if i==2:
            csv_write.writerow(headlist+["税费总计","是否唯一","税费描述"])
        else:
            csv_write.writerow(headlist)
        houselinks=getlinks(detailinkfilename)
        m=1
        for titurl in houselinks:
            titurl = eval(titurl)
            title=titurl[0]
            url=titurl[1].strip()
            if m>=1 and m<=1110:
                print("第"+str(m)+"条房屋信息")
                for i in range(3):           
                    if detailcrawl(url,title,csv_write,headlist) =="error":
                        time.sleep(5)
                        if i==2:
                            print(url+"链接不可用")
                        continue
                    else:
                        break
            m+=1
            
filename='./data/links.txt'
main(filename)

 


