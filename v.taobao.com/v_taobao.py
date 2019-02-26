import re
from bs4 import BeautifulSoup
import requests
import json
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
import time
cook='thw=cn; cna=h9/yEVZzcBsCAXrNB8OEFnAP; hng=CN%7Czh-CN%7CCNY%7C156; t=8464a4877acc365c142612d5c3535d73; tracknick=chang19961122; tg=0; enc=o0CVVmQHW%2Fmm%2By358BfYN%2FCz5Z5xHKNJqwXsT8JCEwKnfFXbRNgcQNNwYBdv%2Fzd%2FqsmSD5l1CaFZytf7z%2FSYqA%3D%3D; uc3=vt3=F8dByRzKEOtARWtl%2Bgw%3D&id2=UUphyI2MZooAgg%3D%3D&nk2=AHLWi98GGcUQYFQdBA%3D%3D&lg2=UIHiLt3xD8xYTw%3D%3D; lgc=chang19961122; _cc_=V32FPkk%2Fhw%3D%3D; mt=np=; JSESSIONID=78E35E447B5B636D8D0608B053B487CF; v=0; cookie2=33f1dba922315c46dafb0f77a84ec122; _tb_token_=ebfee6d5ba3bb; uc1=cookie14=UoTYMhm537QgtA%3D%3D; isg=BHFxPzFAiROB_yBuY-kvN_FAgP3BLOeuiKVbc1ODrjtzep_Mm68JoNDcmE65sn0I'
cook='_tb_token_=undefined; thw=cn; cna=h9/yEVZzcBsCAXrNB8OEFnAP; hng=CN%7Czh-CN%7CCNY%7C156; t=8464a4877acc365c142612d5c3535d73; tracknick=chang19961122; tg=0; enc=o0CVVmQHW%2Fmm%2By358BfYN%2FCz5Z5xHKNJqwXsT8JCEwKnfFXbRNgcQNNwYBdv%2Fzd%2FqsmSD5l1CaFZytf7z%2FSYqA%3D%3D; uc3=vt3=F8dByRzKEOtARWtl%2Bgw%3D&id2=UUphyI2MZooAgg%3D%3D&nk2=AHLWi98GGcUQYFQdBA%3D%3D&lg2=UIHiLt3xD8xYTw%3D%3D; lgc=chang19961122; _cc_=V32FPkk%2Fhw%3D%3D; mt=np=; v=0; cookie2=33f1dba922315c46dafb0f77a84ec122; _tb_token_=ebfee6d5ba3bb; JSESSIONID=349843D9A54549D07028E4C69185BDBF; uc1=cookie14=UoTYMhm51zYOYQ%3D%3D; isg=BG5uv-Ppvkrp5c9HaHj4PmqBv8T6HTAXQ0Q02pg323Esew7VAP2neRV6N6cyoyqB'
header={
    'Cookie':cook,
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'referer':'https://v.taobao.com/v/content/live?spm=a21xh.11312891.quickLink.1.1ae97001PFhgoc&catetype=701',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'x-requested-with':'XMLHttpRequest'
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
def phangetObj(url,header):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
    )
    dcap["phantomjs.page.settings.cookie"] = (
    header['cookie']
    )

    driver =webdriver.PhantomJS(executable_path="phantomjs.exe",desired_capabilities=dcap)   
    #使用浏览器请求页面
    driver.get(url)
    #加载3秒，等待所有数据加载完毕
    time.sleep(3)
    #通过id来定位元素，
    #.text获取元素的文本数据
    # dl=driver.find_elements_by_css_selector("#searchLeftOptions")
    # dl=driver.find_element_by_id("searchLeftOptions")
    # dl.click()
    pageSource=driver.page_source

    return pageSource
# url='https://v.taobao.com/micromission/req/selectCreatorV3.do?cateType=701&sortField=2&fansCount=%E4%B8%8D%E9%99%90&currentPage=3&_ksTS=1544782375354_283&_output_charset=UTF-8&_input_charset=UTF-8'
def get_link():
    f=open('V_link.txt','a+',encoding='utf-8',newline='')

    for i in range(1,151):
        # url='https://v.taobao.com/micromission/req/selectCreatorV3.do?cateType=701&sortField=2&fansCount=%E4%B8%8D%E9%99%90&currentPage='+str(i)+'&_output_charset=UTF-8&_input_charset=UTF-8'
        url='https://v.taobao.com/micromission/req/selectCreatorV3.do?cateType=701&sortField=2&fansCount=10%E4%B8%87%E4%BB%A5%E4%B8%8B&currentPage='+str(i)+'&_output_charset=UTF-8&_input_charset=UTF-8'
        req=requests.get(url,headers=header)
        js=json.loads(req.text)['data']['result']
        for j in js:
            f.write(str(j)+'\n')
        print(req.text)
    f.close()

def analysis():
    workbook = xlsxwriter.Workbook('v_link.xlsx')     #创建工作簿
    sheet = workbook.add_worksheet()
    r=0
    for line in open('V_link.txt','r',encoding='utf-8'):
        # print(line)
        line=line.replace('\n','').replace("'",'"').replace('"isV": True,','').replace('"isV": False,','')
        print(line)
        # try:
        js=json.loads(line)
        # except:
        #     print(line)
        # print(js)
        url=js['homeUrl']
        sheet.write(r,0,url)
        r=r+1
    workbook.close()
# analysis()

def get_main_data():
    
    
    cook='_tb_token_=undefined; thw=cn; cna=h9/yEVZzcBsCAXrNB8OEFnAP; hng=CN%7Czh-CN%7CCNY%7C156; t=8464a4877acc365c142612d5c3535d73; tracknick=chang19961122; tg=0; enc=o0CVVmQHW%2Fmm%2By358BfYN%2FCz5Z5xHKNJqwXsT8JCEwKnfFXbRNgcQNNwYBdv%2Fzd%2FqsmSD5l1CaFZytf7z%2FSYqA%3D%3D; uc3=vt3=F8dByRzKEOtARWtl%2Bgw%3D&id2=UUphyI2MZooAgg%3D%3D&nk2=AHLWi98GGcUQYFQdBA%3D%3D&lg2=UIHiLt3xD8xYTw%3D%3D; lgc=chang19961122; _cc_=V32FPkk%2Fhw%3D%3D; mt=np=; v=0; cookie2=33f1dba922315c46dafb0f77a84ec122; _tb_token_=ebfee6d5ba3bb; JSESSIONID=349843D9A54549D07028E4C69185BDBF; uc1=cookie14=UoTYMhm51zYOYQ%3D%3D; isg=BG5uv-Ppvkrp5c9HaHj4PmqBv8T6HTAXQ0Q02pg323Esew7VAP2neRV6N6cyoyqB'
    header={
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9',
        'cache-control':'max-age=0',
        'cookie':cook,
        'referer':'https://v.taobao.com/v/content/live?spm=a21xh.11312891.quickLink.1.1ae97001PFhgoc&catetype=701',
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        
    }
    for line in open('final_link.txt','r',encoding='utf-8'):
        # req=requests.get(line,headers=header,timeout=15)
        req=phangetObj(line,header)
        
        bsObj=BeautifulSoup(req,'html.parser')
        # print(bsObj)
        nick=bsObj.find('h3',class_='nick').find('span').get_text()
        fan_num=bsObj.find('div',class_='fans').find('span',class_='nums').get_text()
        ability=bsObj.find('div',class_='v3-ability-box')
        ability_num=ability.find('div',class_='abilitynum').find('span',class_='num').get_text()
        row=[line,nick,fan_num,ability_num]
        abity_list=ability.find_all('div',class_='next-row next-row-no-wrap abilitydata', recursive=False)
        if len(abity_list)!=2:
            print('没找到2个')
            print(line)
            
        for a in abity_list:
            red_list=a.find_all('div',class_='text-red')
            for red in red_list:
                row.append(red.get_text())

        #7日工作量
        # history=bsObj.find('div',class_='v3-home-historicalWorks')
        # his_list=history.find_all('span',class_='di-num')
        # if len(his_list)!=5:
        #     print('历史7日数据不为5')
        #     print(line)
            
        # for h in his_list:
        #     row.append(h.get_text())

        #直播类型，简介
        
        type_list=bsObj.find_all('div',class_='v3vcom')
        if len(type_list)!=3:
            print('类型不为3')
            print(line)
        for t in type_list:
            row.append(t.get_text())
        
        print(row)
# get_main_data() 
def get_main_json():  
    f=open('main_data_add.txt','a+',encoding='utf-8',newline='')
    f1=open('error.txt','a+',encoding='utf-8',newline='')
    for line in open('final_link.txt','r',encoding='utf-8'):
        line=line.replace('\n','')
        url='https://v.taobao.com/micromission/daren/daren_main_portalv3.do?userId='+re.search(r'userId=(.+?)&pvid=',line).group(1)        
        cook='thw=cn; cna=h9/yEVZzcBsCAXrNB8OEFnAP; hng=CN%7Czh-CN%7CCNY%7C156; t=8464a4877acc365c142612d5c3535d73; tracknick=chang19961122; tg=0; enc=o0CVVmQHW%2Fmm%2By358BfYN%2FCz5Z5xHKNJqwXsT8JCEwKnfFXbRNgcQNNwYBdv%2Fzd%2FqsmSD5l1CaFZytf7z%2FSYqA%3D%3D; uc3=vt3=F8dByRzKEOtARWtl%2Bgw%3D&id2=UUphyI2MZooAgg%3D%3D&nk2=AHLWi98GGcUQYFQdBA%3D%3D&lg2=UIHiLt3xD8xYTw%3D%3D; lgc=chang19961122; _cc_=V32FPkk%2Fhw%3D%3D; mt=np=; _m_h5_tk=5683922c5f623a6fbe94d5641bf0f45f_1544800107501; _m_h5_tk_enc=7d554f516aed0b711d796d40c24d8ba4; v=0; cookie2=3e0031bcf1358ebd2b0a99b10d1e1fc2; _tb_token_=e33d8e533f557; uc1=cookie14=UoTYMha5CCrJNw%3D%3D; JSESSIONID=DF6F565D49E4CC6F39D0FAD13495CE33; isg=BKys8eVc3Gtj9c05FgKaGJxrfYrUai08VX62RAbt-9f4EUwbLnWsn6TgNZkM0ohn'
        header={
            'Cookie':cook,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'referer':'https://v.taobao.com/v/home/?spm=a21xh.11312873.701.1.58887001VNp6tZ&userId=69226163&pvid=&scm=',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'x-requested-with':'XMLHttpRequest'
        }
        req=requests.get(url,headers=header)
        js=json.loads(req.text)['data']
        nick=js['darenNick']
        try:
            fan_num=js['fansCount']
        except:
            print(line)   
            f1.write(line+'\n')         
            continue
        ability_num=js['darenScore']
        #不写入
        miss_type=js['darenMissionData']
        ty=miss_type['servType']
        area=js['area']
        try:
            jie=json.loads(js['desc'])['blocks']
            text=''
            for j in range(len(jie)):
                text=text+jie[j]['text']
            jianjie=re.sub('[ ]+',' ',text)
        except:
            jianjie=js['desc']
            # print(js['desc'])
                        

        receiveRate=miss_type['receiveRate']
        responseTime=miss_type['responseTime']
        completeRate=miss_type['completeRate']
        try:
            avgScore=miss_type['avgScore']
        except:
            avgScore='--'
        cooperateSellerCount=miss_type['cooperateSellerCount']
        completeMission=miss_type['completeMission']
        contentData=js['contentData']
        publish=contentData['publish']
        ipv=contentData['ipv']
        text_pv=contentData['text_pv']
        live_pv=contentData['live_pv']
        video_pv=contentData['video_pv']

        row=[line,nick,fan_num,ability_num,receiveRate,responseTime,completeRate,avgScore,cooperateSellerCount, completeMission,publish,ipv,text_pv,live_pv,video_pv,ty,area,jianjie]
        print(row)
        f.write(str(row)+'\n')
    f.close()
# get_main_json()
        


def write_xlsx():
    workbook = xlsxwriter.Workbook('v_taobao_add.xlsx')     #创建工作簿
    sheet = workbook.add_worksheet()
    r=0
    rowname=['链接','昵称','粉丝数','综合能力','接单率','响应时间','完成率','服务评分','累计用户数','服务数量','7日内容发布数','7日内容引导进店次数','图文7日内容浏览次数','直播7日内容观看次数','短视频7日内容播放次数','服务类型','服务领域','自我介绍']
    for i in range(len(rowname)):
            sheet.write(r,i,rowname[i])
    r=1
    for line in open('main_data_add.txt','r',encoding='utf-8'):
        line=eval(line)
        # if line[-1]=='' and r<2000:
        #     print(r)
        #     url='https://v.taobao.com/micromission/daren/daren_main_portalv3.do?userId='+re.search(r'userId=(.+?)&pvid=',line[0]).group(1)        
        #     cook='thw=cn; cna=h9/yEVZzcBsCAXrNB8OEFnAP; hng=CN%7Czh-CN%7CCNY%7C156; t=8464a4877acc365c142612d5c3535d73; tracknick=chang19961122; tg=0; enc=o0CVVmQHW%2Fmm%2By358BfYN%2FCz5Z5xHKNJqwXsT8JCEwKnfFXbRNgcQNNwYBdv%2Fzd%2FqsmSD5l1CaFZytf7z%2FSYqA%3D%3D; uc3=vt3=F8dByRzKEOtARWtl%2Bgw%3D&id2=UUphyI2MZooAgg%3D%3D&nk2=AHLWi98GGcUQYFQdBA%3D%3D&lg2=UIHiLt3xD8xYTw%3D%3D; lgc=chang19961122; _cc_=V32FPkk%2Fhw%3D%3D; mt=np=; _m_h5_tk=5683922c5f623a6fbe94d5641bf0f45f_1544800107501; _m_h5_tk_enc=7d554f516aed0b711d796d40c24d8ba4; v=0; cookie2=3e0031bcf1358ebd2b0a99b10d1e1fc2; _tb_token_=e33d8e533f557; uc1=cookie14=UoTYMha5CCrJNw%3D%3D; JSESSIONID=DF6F565D49E4CC6F39D0FAD13495CE33; isg=BKys8eVc3Gtj9c05FgKaGJxrfYrUai08VX62RAbt-9f4EUwbLnWsn6TgNZkM0ohn'
        #     header={
        #         'Cookie':cook,
        #         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        #         'referer':'https://v.taobao.com/v/home/?spm=a21xh.11312873.701.1.58887001VNp6tZ&userId=69226163&pvid=&scm=',
        #         'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        #         'x-requested-with':'XMLHttpRequest'
        #     }
        #     req=requests.get(url,headers=header)
        #     js=json.loads(req.text)['data']
        #     if js['desc'][:3]=='htt':
        #         line[-1]='_'+js['desc']
        for i in range(len(line)):
            sheet.write(r,i,line[i])
        r=r+1
    workbook.close()     


write_xlsx()

    





