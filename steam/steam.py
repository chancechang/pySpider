
import requests

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

url='https://store.steampowered.com/appreviews/578080?start_offset=20&day_range=0&start_date=1510379757&end_date=1519465323&date_range_type=include&filter=recent&language=schinese&l=schinese&review_type=all&purchase_type=steam&review_beta_enabled=0&summary_num_positive_reviews=374156&summary_num_reviews=761500'
# url='https://store.steampowered.com/appreviews/578080?start_offset=0&day_range=30&start_date=1509026588.4112&end_date=1515792435.1402&date_range_type=include&filter=summary&language=english&l=english&review_type=all&purchase_type=steam&review_beta_enabled=0&summary_num_positive_reviews=374183&summary_num_reviews=761572'
url='https://store.steampowered.com/appreviews/578080?start_offset=20&day_range=0&start_date=1507576764&end_date=1519175358&date_range_type=include&filter=recent&language=english&l=english&review_type=all&purchase_type=steam&review_beta_enabled=0&summary_num_positive_reviews=374183&summary_num_reviews=761572'
url='https://store.steampowered.com/appreviews/578080?start_offset=40&day_range=0&start_date=1507576764&end_date=1519175358&date_range_type=include&filter=recent&language=english&l=english&review_type=all&purchase_type=steam&review_beta_enabled=0&summary_num_positive_reviews=374183&summary_num_reviews=761572'
nix=1513353600 #2017/12/16 00:00:00
endtime=1518969599 #2018/2/18 23:59:59
req=requests.get(url,proxies=get_proxies_abuyun() )
print(req.text)
