import os,shutil
import xlrd

def copy():

    rootdir='./'
    newdir='../../Desktop/pySpider'
    if not os.path.exists(newdir):
        os.mkdir(newdir)
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
        print(list[i])
        # try:
        path1 = os.path.join(rootdir,list[i])
        # except:
        #     continue
        if list[i].endswith('.py'):
            shutil.copyfile(path1,os.path.join(newdir,list[i]))
            # break
        
        if os.path.isdir(path1):
            dir=os.path.join(newdir,list[i])
            if not os.path.exists(dir):
                os.mkdir(dir)
            list1 = os.listdir(path1)
            for j in range(0,len(list1)):
                path2=os.path.join(path1,list1[j])
                if list1[j].endswith('.py'):
                    shutil.copyfile(path2,os.path.join(dir,list1[j]))
                
copy()