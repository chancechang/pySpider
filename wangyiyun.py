import requests
from bs4 import BeautifulSoup
import requests
import hashlib
import sys
import click
import re
import base64
import binascii
import json
import os
from Crypto.Cipher import AES
from http import cookiejar

# 总用户为42258

# url = 'https://music.163.com/weapi/user/getfolloweds?csrf_token=7fc815a256138cc623ec30592dc834a8'
# params = '41eCwYphfKMYrKWRpr+i4zzDSlmDcL3uJz/5XWR6VqzsjXbK455KKKKjO147F2L0jzVSvA6LR+7uWlCYZIN9Yl5SeKoF3wRgxnPwHF9kXt0IesE2Z1HgfXqbvmmBLb7oArQaWSWYuMSFYs/RluihAF9z7CJ2uBW/ffozt8YboMXyPslC6cJHF8ioXaOwfIIrUWAWpO09sb+RSOpIgvZpKKm12ibW39jJ4vwxHnUzOKY='
# encSecKey= '342729ae8f8fadbb6510a3148d70fae4876136b30bcabe6a01de1d9ac9b6ef6a67757d9d3cd69ac206d37aa11db9dfe2ceb584216496cccdb764c7ccfb6d5dbd0e25d15f07e5bf351b7aaca825b451b7efa77808c970e96415fe3040bee094b7a0b4e09d2fab25617b53ca86157eecc471bb45c65fe1964e08020772f54c2988'
# data = {
#     'params':params,
#     'encSecKey':encSecKey

# }
# req = requests.post(url,data=data)
# print(req.text)


class Encrypyed():
    """
    解密算法
    """

    def __init__(self):
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'
        self.pub_key = '010001'

    # 登录加密算法, 基于https://github.com/stkevintan/nw_musicbox脚本实现
    def encrypted_request(self, text):
        text = json.dumps(text)
        sec_key = self.create_secret_key(16)
        enc_text = self.aes_encrypt(self.aes_encrypt(
            text, self.nonce), sec_key.decode('utf-8'))
        enc_sec_key = self.rsa_encrpt(sec_key, self.pub_key, self.modulus)
        data = {'params': enc_text, 'encSecKey': enc_sec_key}
        return data

    def aes_encrypt(self, text, secKey):
        pad = 16 - len(text) % 16
        text = text + chr(pad) * pad
        encryptor = AES.new(secKey.encode('utf-8'),
                            AES.MODE_CBC, b'0102030405060708')
        ciphertext = encryptor.encrypt(text.encode('utf-8'))
        ciphertext = base64.b64encode(ciphertext).decode('utf-8')
        return ciphertext

    def rsa_encrpt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = pow(int(binascii.hexlify(text), 16), int(pubKey, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

    def create_secret_key(self, size):
        return binascii.hexlify(os.urandom(size))[:16]


class Crawler():
    """
    网易云爬取API
    """

    def __init__(self, timeout=60, cookie_path='.'):
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.cookies = cookiejar.LWPCookieJar(cookie_path)
        self.download_session = requests.Session()
        self.timeout = timeout
        self.ep = Encrypyed()

    def post_request(self, url, params):
        """
        Post请求
        :return: 字典
        """
        data = self.ep.encrypted_request(params)
        resp = self.session.post(url, data=data, timeout=self.timeout)
        result = resp.json()
        if result['code'] != 200:
            click.echo('post_request error')
        else:
            return result
    def get_playlist(self,userId):
        url = 'https://music.163.com/weapi/user/playlist?csrf_token=7fc815a256138cc623ec30592dc834a8'
        params = {
                'limit': 1000,
                'offset': 0,
                'total': True,
                'uid': userId,
                'wordwrap': 7
            }
        return self.post_request(url,params)


    def get_funs(self, userId, pageNum=10):
        url = 'https://music.163.com/weapi/user/getfolloweds?csrf_token=7fc815a256138cc623ec30592dc834a8'
        funs_data = []
        for i in range(0, pageNum):
            offset = i * 100
            params = {
                'limit': 100,
                'offset': offset,
                'total': True,
                'userId': userId
            }
            followeds = self.post_request(url,params)['followeds']
            funs_data += followeds
            if len(followeds) < 100:
                return funs_data
        return funs_data

    def get_second_funs(self,userId):
        funs_data1 = []
        funs_data2 = []
        print(userId)
        first_followeds = self.get_funs(userId)
        for followed in first_followeds:
            funs_data1.append([userId,followed])
            if followed['followeds'] != 0:               
                second_followeds = self.get_funs(followed['userId'])
                for sec_followed in second_followeds:
                    funs_data2.append([userId,str(followed['userId']),sec_followed])
        return funs_data1,funs_data2


#海岛度假Santorini  -KooTo-  三岁小猪乔治 情思天鹅
# if __name__ == '__main__':
m = False
if m:
    userId_list = ['31379262','17711631','1426292524','108952364']
    funs_data1 = []
    funs_data2 = []
    for userId in userId_list:   
        craw = Crawler(60, 'Cookie')
        data1,data2 = craw.get_second_funs(userId)
        funs_data1 += data1
        funs_data2 += data2
    f = open('first_funs.txt','r')    
    for fun in funs_data1:
        f.write(json.dumps(fun)+'\n')
    f.close()
    f = open('second_funs.txt','r')
    for fun in funs_data2:
        f.write(json.dumps(fun)+'\n')
    f.close()

if m:
    user_list = []
    craw = Crawler(60, 'Cookie')
    for line in open('second_funs.txt','r'):
        line = json.loads(line)
        user_list += line[:2] +[str(line[2]['userId'])]#修正：应该加str的
    print(len(user_list))#144546
    userid_list = list(set(user_list)) 
    print(len(userid_list)) # 42422 有粉丝的用户  修正后为42258
    #爬取原始数据
    f = open('user_palylist_raw.txt','r')
    n = 0
    for userId in userid_list:
        n = n+1
        if n % 1000 == 0:
            print(n)
        f.write(json.dumps([str(userId),craw.get_playlist(userId)])+'\n')
    f.close()


if False:
    #所有的收藏数据
    f = open('user_playlist_collect.txt','w+')#收藏大于20个歌单，16452个用户,修正后16357 #2386559条数据，修正后2356367
    j = 0
    for line in open('user_palylist_raw.txt','r'):       
        line = json.loads(line)
        user = line[0]
        playlists = line[1]['playlist']
        i = 0
        data = []
        for play in playlists:
            creator = play['userId']
            if str(creator) != str(user): #不是自己创建的，而是收藏的
                i += 1
                data.append([user,play['id']])
        # print(i) 
        if i < 20:
            continue
        j += 1
        for d in data:
            f.write(json.dumps(d)+'\n')
        #     print(play['id'],play['userId'],play['name'],play['playCount'],play['trackCount'],)
    f.close()
    print(j)

# craw = Crawler(60, 'Cookie')
# print(json.loads(craw.get_playlist("31379262"))==json.loads(craw.get_playlist(31379262)))