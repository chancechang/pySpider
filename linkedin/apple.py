import requests
from bs4 import BeautifulSoup
import re



def get_picture(bsObj):
    lk_list=[]
    f=open('picture.txt','w+',encoding='utf-8')
    link_list=bsObj.find_all('img')
    for l in link_list:
        try:
            if 'http' in l.attrs['src']:
                lk_list.append(l.attrs['src'])
            else:
                lk_list.append('https://support.apple.com'+l.attrs['src'])
                # f.write(l.attrs['href']+'\n')
        except:
            pass
    for l in set(lk_list):
        f.write(l+'\n')
    f.close()


def get_link(url,lk_list):
    if url.strip() in lk_list or 'apple' not in url or '404'  in url or url.strip()[:-1] in lk_list:
        return lk_list
    lk_list.append(url)
    f.write(url+'\n')
    print(url)
    for i in range(3):
        try:
            html=requests.get(url,timeout=15)
            htmlcont=html.text
            bsObj=BeautifulSoup(htmlcont,'html.parser')
            break
        except:
            print('try again')
            continue
        if i == 2:
            print('request_error')
            return lk_list
    
    link_list=bsObj.find_all('link')
    # print(link_list)
    for l in link_list:
        try:
            if 'http' in l.attrs['href']:
                url1=l.attrs['href']               
                url1=url1[:9]+re.sub('/+','/',url1[9:])
                lk_list=get_link(url1,lk_list)
            else:
                if l.attrs['href'][0]=='#' or l.attrs['href'] in url:
                    pass
                else:
                    url1=url1[:9]+re.sub('/+','/',url1[9:])
                    url1='https://support.apple.com/'+l.attrs['href']
                    lk_list=get_link(url1,lk_list)
        except:
            print('link_error')
        
            pass
    link_list=bsObj.find_all('a')
    # print(link_list)
    for l in link_list:
        try:
            if 'http' in l.attrs['href']:
                url1=l.attrs['href']
                # print(url1)
                url1=url1[:9]+re.sub('/+','/',url1[9:])
                print(url1)
                lk_list=get_link(url1,lk_list)
                # lk_list.append(l.attrs['href'])                
                # f.write(l.attrs['href']+'\n')
            else:
                if l.attrs['href'][0]=='#'or l.attrs['href'] in url:
                    pass
                else:
                    url1='https://support.apple.com/'+l.attrs['href']
                    url1=url1[:9]+re.sub('/+','/',url1[9:])
                    lk_list=get_link(url1,lk_list)
                # url1=url+l.attrs['href']
                # lk_list=get_link(url1,lk_list)                
                # lk_list.append('https://support.apple.com'+)                
                # f.write('https://support.apple.com'+l.attrs['href']+'\n')     
        except:
            print('a_error')            
            pass
    return lk_list


    

url='https://support.apple.com/'
f=open('link.txt','w+',encoding='utf-8')
lk_link=get_link(url,[])
# for l in set(lk_link):
#     f.write(l+'\n')
f.close()

# link href
# a href
# img src
# form action
# meta content