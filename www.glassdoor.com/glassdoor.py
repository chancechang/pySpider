from bs4 import BeautifulSoup
import requests
import xlsxwriter



cook='GSESSIONID=C137100C3A6D01AF799CC5F538542768; gdId=47174bb8-4696-4b0a-8a97-339e26555d9b; trs=direct:direct:direct:2018-11-19+03%3A28%3A00.358:undefined:undefined; _ga=GA1.2.774351675.1542626890; _gid=GA1.2.516653024.1542626890; _gcl_au=1.1.1941462808.1542626892; ht=%7B%22quantcast%22%3A%5B%22D%22%5D%7D; __qca=P0-684848410-1542626893174; _fbp=fb.1.1542626893614.576131675; __gads=ID=df9c28cb08310077:T=1542626892:S=ALNI_MZW0jujF9qfuCULrOoVvKXgIbcVlA; cto_lwid=0fd3ebc6-4bdb-41f4-a910-485617d8224e; __gdpopuc=1; _uac=000001672bc013c1a023827149333411; uc=D9A9850D0C92C1EF344B33D6D6A738C9266A5B35FCACEBC67B8233944D413B1FDC746FDC2F893325DA9EC29B9CEF01014C69591E7C823839940BC19BFC8050F300A91A56EF9E781F1B093ADF4592A4AC400257BD03270137A96287D6C1E1F0D7C99CD43CFF00A61976E24F60CEE3A6789E0289F3F55D6FF5E1478C8CC180A403510E5E5879A69F7118EF9BD2F1285B25A3EB452B8F8044384CD29523AE411052; newUserOnboarding=false; _mibhv=anon-1542627279784-4981872518_6890; _urc=84303168; _dc_gtm_UA-2595786-1=1; _gat_UA-2595786-1=1; cass=1; AWSALB=KdefgN9fi9CBfD1hX4J+PMkklkO2IPMzmSnXMgKHpfDew0WpKYTX0xfLlg2zbG5FUukAcJr4BbCPSjk/2xIc7/U7b0QQpvk534HcgBmzx/VZKHcsdWp+AOrLX+a2Py/LnnfLsrc/eKxc9bkyIWoh0Nbb0Tsgksxen3F+vmPLXzJ2RT7D7zr6lYWl/lnNOFb3LwfVwPfwAVWmIzmGOObQht0SN2g2GXdHEbwd39rs7ab4XPaPy95o3yRvD8j6KR3TbPrRp9CIQV37bXXtRXSfxktcrJu5LMZkRwEtz6ljRnuNYADg8KiGkAt6qwuuMWL/'
header={
    'Cookie':cook,
    'referer':'https://www.glassdoor.com/',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}

def main():
    f=open('glassdoor.txt','w+',encoding='utf-8')
    score_title=['Work','Cult','Care','Comp','Seni']   
    for i in range(1,29):
        print('正在爬第'+str(i)+'页')
        url='https://www.glassdoor.com/Reviews/Alibaba-Group-Reviews-E225974_P'+str(i)+'.htm'
        req=requests.get(url,headers=header)
        bsObj=BeautifulSoup(req.text,'html.parser')
        li_list=bsObj.find_all('li',class_=' empReview cf ')
        for li in li_list:
            time=li.find('time',class_='date subtle small').attrs['datetime']
            name=li.find('span',class_='summary ').get_text()
            t_score=li.find('span',class_='gdStars gdRatings sm margRt').find('span',class_='value-title').attrs['title']
            employee=li.find('span',class_='authorJobTitle middle reviewer').get_text()
            pros=li.find('p',class_=' pros mainText truncateThis wrapToggleStr').get_text()
            con=li.find('p',class_=' cons mainText truncateThis wrapToggleStr').get_text()
            row=[name,time,employee,t_score,pros,con]   
            score_l=['' for j in range(5)]

            scoreul=li.find('ul',class_='undecorated')
            if scoreul!=None:
                
                for s in scoreul.find_all('li'):
                    tx=s.find('div',class_='minor').get_text().strip()[:4]
                    t=score_title.index(tx)
                    score_l[t]=s.find('span',class_='gdBars gdRatings med ').attrs['title']

            row=row+score_l
            f.write(str(row)+'\n')
        # break
    f.close()

def writeToexcel():
    filename='glassdoor'
    workbook=xlsxwriter.Workbook(filename+'.xlsx')
    sheet=workbook.add_worksheet()
    r=0
    for line in open('glassdoor1.txt','r',encoding='utf-8'):
        line=eval(line)
        le=len(line)
        for i in range(le):
            sheet.write(r,i,line[i])
        r=r+1
    workbook.close()


main()

writeToexcel()

