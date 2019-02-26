
import requests
import csv
import time
import json
import re
import sys
from urllib.error import HTTPError
sys.path.append("..")
import mytemp

url='https://huggies.tmall.com/category-1038993307.htm?spm=a1z10.3-b-s.w4011-14533183956.292.787976ceiOvHAT&type=p&newHeader_b=s_from&searcy_type=item&from=.shop.pc_2_searchbutton&catId=1038993307&keyword=%BA%C3%C6%E6&pageNo=2&tsearch=y#anchor'
cook='cna=h9/yEVZzcBsCAXrNB8OEFnAP; hng=CN%7Czh-CN%7CCNY%7C156; _m_h5_tk=64705fff8ba6e9dd50853f5f5b9929cb_1539873398765; _m_h5_tk_enc=5301f3c7015e41bb1026840101c64f24; t=8464a4877acc365c142612d5c3535d73; _tb_token_=753361be35e5a; cookie2=1a3195a39b1ad24bf437640212c57659; pnm_cku822=; cq=ccp%3D1; isg=BFRUCI2p88yHkGdJey2xbUrjJZLMozARvabeTO41QF9Z2fUjFr4_J6Mf3ZFkIbDv'
header={
    'Cookie':cook,
# referer:https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-14466283798.50.43547440H0DfBt&id=40545566432&rn=6fe19d846dcf80351798b26fa5bfdf95&abbucket=20&skuId=3854687709703'
}
bsObj=mytemp.getObj(url,False,cook)
print(bsObj)
# print(bsObj.find('div',class_='J_TItems'))