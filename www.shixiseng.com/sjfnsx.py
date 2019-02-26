
import util
import csv
import jieba
import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
url='https://www.shixiseng.com/interns/st-intern_?k=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&t=zh&p='
cook='SXS_VISIT_XSESSION_ID_V3.0="2|1:0|10:1528005972|26:SXS_VISIT_XSESSION_ID_V3.0|48:OWNlMmNlMjQtNjM3Mi00YmEwLThiMWQtOTJjZjM4MjQ4Mjlm|2adb2da0ba19962795406b9a9589e3ee9d493196228a738dfd7023a4991a1d50"; SXS_XSESSION_ID="2|1:0|10:1528005972|15:SXS_XSESSION_ID|48:OWNlMmNlMjQtNjM3Mi00YmEwLThiMWQtOTJjZjM4MjQ4Mjlm|d00e5e0246c3c01d22934b0a3d73d3c39da1be03b18937b2a8691875b69ae82a"; SXS_XSESSION_ID_EXP="2|1:0|10:1528005972|19:SXS_XSESSION_ID_EXP|16:MTUyODA5MjM3Mg==|9205c048dcf474f81c81d62d071062b051e2ca2b92195d8b8107f8be2f35a544"; SXS_VISIT_XSESSION_ID_V3.0_EXP="2|1:0|10:1528005972|30:SXS_VISIT_XSESSION_ID_V3.0_EXP|16:MTUzMDU5Nzk3Mg==|33f2f025eb50c8766401b89089435adc0b6da2a4e6f2b6e8dc3d446f246b93a3"; __jsluid=5611e6cc21fa544c2dce0492976234e7; Hm_lvt_03465902f492a43ee3eb3543d81eba55=1528005975; Hm_lpvt_03465902f492a43ee3eb3543d81eba55=1528005975; gr_user_id=7859d17e-fb1b-4d34-acf2-023633a93164; gr_cs1_89128412-e437-4e75-b450-9c2baa30c709=user_id%3Anull; uuid=fa1d61cf-5354-756b-a51e-01c4dfea3bb8; gr_session_id_96145fbb44e87b47=89128412-e437-4e75-b450-9c2baa30c709_true; MEIQIA_EXTRA_TRACK_ID=15UkHUreiIy909cz0gN9vdcfVOs'

replace_dict = {
    '\uf1c4': '0',
    '\uf541': '1',
    '\uefb0': '2',
    '\ueae6': '3',
    '\ue95c': '4',
    '\uf11b': '5',
    '\ue39f': '6',
    '\uf417': '7',
    '\uecc0': '8',
    '\uec65': '9',
    '\ue385': '网',
    '\uf029': '行',
    '\uf6f2': 'G',
    '\uf14e': 'r',
    '\ue2a3': 'o',
    '\uf0df': 'u',
    '\ue60a': 'p',
    '\uec45': 'M',
    '\uf1d5': 'T',
    '\ue4b7': 'B',
    '\uf7fb': 'S',
    '\ueca0': '人',
    '\uf0ef': '广',
    '\uef40': '告',
    '\uebcc': '工',
    '\ue165': '作',
    '\ue46f': '师',
    

}

def sreplace(s):
    for key,value in replace_dict.items():
        s=s.replace(key,value)
    return(s)


def main():
    for i in range(1,47):
        lilist=util.getObj(url+str(i),cook).find('ul',class_='position-list').find_all('li')
        print(len(lilist))
        for li in lilist:
            info1=li.find('div',class_='info1')
            nameUrl=info1.find('a',class_='name')
            name=nameUrl.get_text()
            href=nameUrl.attrs['href']
            company=info1.find('a',class_='company').get_text()
            ctype=info1.find('span',class_='type').get_text()

            info2=li.find('div',class_='info2')
            area=info2.find('div',class_='area').get_text()
            more=info2.find('div',class_='more')
            salary=more.find_all('span')[0].get_text()
            dayperweek=more.find_all('span')[1].get_text()
            alltime=more.find_all('span')[2].get_text()
            row=[sreplace(name),href,sreplace(company),ctype,area,sreplace(salary),sreplace(dayperweek),sreplace(alltime)]
            print(row)
            # out.write(str(row)+'\n')
            csv_write.writerow(row)
        

# out=open('sjfx.csv','w+',encoding='utf-8',newline='')
# f=open('sjfx.txt','r',encoding='utf-8')
# csv_write=csv.writer(out)
# main()


def getdetail():
    out=open('sjfxdetail.csv','w+',encoding='gb18030',newline='')
    csv_write=csv.writer(out)
    for line in open('sjfx.txt','r',encoding='utf-8'):
        line=eval(line)
        url='https://www.shixiseng.com'+line[1]

        obj=util.getObj(url,cook)
        line[0]=obj.find('div',class_='new_job_name').attrs['title']
        line[2]=obj.find('div',class_='job_com_name cutom_font').get_text()
        for i in range(3,len(line)):
            line[i]=sreplace(line[i])
        job_introduce=obj.find('div',class_='con-job job_introduce').find('div',class_='job_part').get_text().replace('\xa0','').replace('\n','').strip()
        job_deadline=obj.find('div',class_='con-job deadline').find('div',class_='job_detail cutom_font').get_text()
        row=line+[job_introduce,sreplace(job_deadline)]
        csv_write.writerow(row)

# getdetail()

def get_keyword(text):
    keyword=jieba.analyse.extract_tags(text, topK=20, withWeight=False, allowPOS=()) 
    return keyword

def getAllKey():
    jieba.load_userdict("userdict.txt")
    #找出要求的关键词
    out=open('sjfxdetail1.csv','w+',encoding='gb18030',newline='')
    csv_write=csv.writer(out)
    f=open('keyword.txt','w+')
    for line in csv.reader(open('sjfxdetail.csv','r',encoding='gb18030')):
        keyWord=' '.join(get_keyword(line[8]))
        line[9]=sreplace(line[9])
        print([line[9]])
        line.append(keyWord)
        csv_write.writerow(line)
        f.writelines(keyWord)
    f.close()
# getAllKey()
def draw_wordcloud():
    a=''
    for line in open('keyword.txt','r'):
        a=line
    poplist=[]
    for line in open('popdict.txt','r',encoding='utf-8'):
        poplist.append(line.replace('\n',''))

    wordcloud = WordCloud(  font_path='msyh.ttf',
                            background_color='white',
                            width=1200,
                            height=600,
                            stopwords=poplist
                            ).generate(a)

    plt.figure(figsize = (20,10))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

def developed(text):
    if text.find('北京')!=-1 or text.find('上海')!=-1 or text.find('广州')!=-1 or text.find('深圳')!=-1:
        return (1)
    else:
        return (0)
def findKey(text,key):
    if text.find(key)!=-1:
        return (1)
    else:
        return (0)
out=open('sjfxdetail2.csv','w+',encoding='gb18030',newline='')
csv_write=csv.writer(out)
for line in csv.reader(open('sjfxdetail1.csv','r',encoding='gb18030')):
    
    line.append(developed(line[3]))
    line.append(findKey(line[9],'sql') or findKey(line[9],'Sql') or findKey(line[9],'SQL'))
    line.append(findKey(line[9],'Excel'))
    line.append(findKey(line[9],'Python') or findKey(line[9],'python') or findKey(line[9],'PYTHON'))
    line.append(findKey(line[9],'SPSS') or findKey(line[9],'spss') or findKey(line[9],'Spss'))
    line.append(findKey(line[9],'本科'))
    csv_write.writerow(line)