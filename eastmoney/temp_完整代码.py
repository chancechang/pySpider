import requests
import time

def get_data():
    res_text = requests.get(
        'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=0000011,3990012&sty=CTBFTA&st=z&sr=&p=&ps=&cb=&token=70f12f2f4f091e459a279469fe49eca5').text
    data = eval(res_text)
    dh = data[0].split(',')
    ds = data[1].split(',')
    index_map={
        '超大单流入':7,
        '超大单流出':8,
        '大单流入':11,
        '大单流出':12,
        '中单流入':15,
        '中单流出':16,
        '小单流入':19,
        '小单流出':20
    }
    result={}
    for key in index_map:
        index=index_map[key]
        try:
            value='%.4f' % ((float(dh[index]) + float(ds[index])) / 100000000)
        except:
            value=''
        result[key]=value
    return result
    # # 超大单流入
    # try:
    #     data_1 = '%.4f' % ((float(dh[7]) + float(ds[7])) / 100000000)
    # except:
    #     data_1 = ''
    # # 超大单流出
    # data_2 = '%.4f' % ((float(dh[8]) + float(ds[8])) / 100000000)
    # # 大单流入
    # data_3 = '%.4f' % ((float(dh[11]) + float(ds[11])) / 100000000)
    # # 大单流出
    # data_4 = '%.4f' % ((float(dh[12]) + float(ds[12])) / 100000000)
    # # 中单流入
    # data_5 = '%.4f' % ((float(dh[15]) + float(ds[15])) / 100000000)
    # # 中单流出
    # data_6 = '%.4f' % ((float(dh[16]) + float(ds[16])) / 100000000)
    # # 小单流入
    # data_7 = '%.4f' % ((float(dh[19]) + float(ds[19])) / 100000000)
    # # 小单流出
    # data_8 = '%.4f' % ((float(dh[20]) + float(ds[20])) / 100000000)


while True:
    result=get_data()
    print(result)
    time.sleep(59)

