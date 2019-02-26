

import requests
url='http://openapi.roewe.com.cn/ndms-base-server/getSalesInfo/1/10000000000036/3'
url='https://hbzd.en.alibaba.com/company_profile.html?spm=a2700.supplier-normal.35.3.1dea38bcq9ghSk#top-nav-bar'
req=requests.get(url)
print(req.text)
