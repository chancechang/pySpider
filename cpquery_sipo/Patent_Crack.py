#!/usr/bin/env python3
# coding=utf-8

"""    
    @File: Patent-Crack.py
    @Desc: 
    @Author: lv junling
    @Date Created: 2018/10/22
"""
import os
import pickle
import cv2
import numpy as np
from PIL import Image


# 点降噪
def interference_point(img,img_name, x = 0, y = 0):
    """
    9邻域框,以当前点为中心的田字框,黑点个数
    :param x:
    :param y:
    :return:
    """
    filename =  './out_img/' + img_name.split('.')[0] + '-interferencePoint.jpg'
    # todo 判断图片的长宽度下限
    cur_pixel = img[x,y]# 当前像素点的值
    height,width = img.shape[:2]

    for y in range(0, width - 1):
      for x in range(0, height - 1):
        if y == 0:  # 第一行
            if x == 0:  # 左上顶点,4邻域
                # 中心点旁边3个点
                sum = int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右上顶点
                sum = int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            else:  # 最上非顶点,6邻域
                sum = int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 3 * 245:
                  img[x, y] = 0
        elif y == width - 1:  # 最下面一行
            if x == 0:  # 左下顶点
                # 中心点旁边3个点
                sum = int(cur_pixel) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x, y - 1])
                if sum <= 2 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右下顶点
                sum = int(cur_pixel) \
                      + int(img[x, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y - 1])

                if sum <= 2 * 245:
                  img[x, y] = 0
            else:  # 最下非顶点,6邻域
                sum = int(cur_pixel) \
                      + int(img[x - 1, y]) \
                      + int(img[x + 1, y]) \
                      + int(img[x, y - 1]) \
                      + int(img[x - 1, y - 1]) \
                      + int(img[x + 1, y - 1])
                if sum <= 3 * 245:
                  img[x, y] = 0
        else:  # y不在边界
            if x == 0:  # 左边非顶点
                sum = int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])

                if sum <= 3 * 245:
                  img[x, y] = 0
            elif x == height - 1:  # 右边非顶点
                sum = int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x - 1, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1])

                if sum <= 3 * 245:
                  img[x, y] = 0
            else:  # 具备9领域条件的
                sum = int(img[x - 1, y - 1]) \
                      + int(img[x - 1, y]) \
                      + int(img[x - 1, y + 1]) \
                      + int(img[x, y - 1]) \
                      + int(cur_pixel) \
                      + int(img[x, y + 1]) \
                      + int(img[x + 1, y - 1]) \
                      + int(img[x + 1, y]) \
                      + int(img[x + 1, y + 1])
                if sum <= 4 * 245:
                  img[x, y] = 0
    cv2.imwrite(filename,img)
    return img

class PatentCrack(object):
    def __init__(self, pkl_fn=None):
        if pkl_fn is None:
            print('[error]Must specify the pickle filename.')
            return
        self.pkl_fn = pkl_fn
        if os.path.exists(pkl_fn):
            self._load_pkl()
        else:
            self.gen_pkl_fn()

    def gen_pkl_fn(self):
        imgs_path = u'./data'
        chi_1_imgs = ['1.jpeg', '2.jpeg', '3.jpeg', '4.jpeg', '5.jpeg',
                      '6.jpeg', '7.jpeg', '8.jpeg', '9.jpeg']

        chi_2_imgs = ['10.jpeg', '11.jpeg', '12.jpeg', '13.jpeg', '14.jpeg', '15.jpeg',
                      '16.jpeg', '17.jpeg', '18.jpeg', '19.jpeg']

        op_imgs    = ['1.jpeg', '7.jpeg']

        chi_3_imgs = ['100.jpeg', '101.jpeg', '102.jpeg', '103.jpeg', '104.jpeg', '105.jpeg',
                      '106.jpeg', '107.jpeg', '108.jpeg', '109.jpeg']

        chi_1_arr = np.zeros([10, 20, 11], dtype=np.bool)
        for idx, img_fn in enumerate(chi_1_imgs):
            c1, _, _, _ = self._get_split_img(os.path.join(imgs_path, img_fn))
            chi_1_arr[idx+1] = c1

        chi_2_arr = np.zeros([10, 20, 9], dtype=np.bool)
        for idx, img_fn in enumerate(chi_2_imgs):
            _, c2, _, _ = self._get_split_img(os.path.join(imgs_path, img_fn))
            chi_2_arr[idx] = c2

        op_arr = np.zeros([3, 20, 12], dtype=np.bool)
        for idx, img_fn in enumerate(op_imgs):
            _, _, op, _ = self._get_split_img(os.path.join(imgs_path, img_fn))
            op_arr[idx] = op

        chi_3_arr = np.zeros([10, 20, 10], dtype=np.bool)
        for idx, img_fn in enumerate(chi_3_imgs):
            _, _, _, c3 = self._get_split_img(os.path.join(imgs_path, img_fn))
            chi_3_arr[idx] = c3

        fout = open(self.pkl_fn, 'wb')
        data = {'chi_1': chi_1_arr, 'chi_2': chi_2_arr, 'op': op_arr, 'chi_3': chi_3_arr}
        pickle.dump(data, fout)
        fout.close()

        self._load_pkl()

    def _load_pkl(self):
        data = pickle.load(open(self.pkl_fn, 'rb'))
        self.chi_1_arr = data['chi_1']
        self.op_arr = data['op']
        self.chi_2_arr = data['chi_2']
        self.chi_3_arr = data['chi_3']

    @staticmethod
    def _get_split_img(img_fn):
        im=Image.open(img_fn).convert('L')
        img_arr = np.array(im)
        # print(img_arr)
        img_arr[img_arr < 156] = 1
        img_arr[img_arr >= 156] = 0
        img_arr = img_arr.astype(np.bool)
        chi_1_arr = img_arr[:,  0:17]
        op_arr = img_arr[:, 17:34]
        chi_3_arr    = img_arr[:, 35:53]
        # im2=im.crop((35, 0, 53, 20))

        # im2.save('ttst.jpeg')
        return chi_1_arr, op_arr, chi_3_arr

    @staticmethod
    def _cal_result(num1, num3,op):
        if op == 0:
            return num1+ num3
        elif op == 1:
            return num1 - num3
        elif op == 2:
            return num1 * num3
        else:
            return int(num1 / num2)

    def feed(self, img_fn):
        chi_1_arr,  op_arr, chi_3_arr = self._get_split_img(img_fn)
        
        # path='./img/01.jpeg'
        # with open(path, "wb") as f:  # 开始写文件，wb代表写二进制文件
        #     f.write(chi_1_arr)
        chi_1_arr = np.tile(chi_1_arr[np.newaxis, :], [10, 1, 1])
        op_arr = np.tile(op_arr[np.newaxis, :], [3, 1, 1])
        # chi_2_arr = np.tile(chi_2_arr[np.newaxis, :], [10, 1, 1])
        chi_1_sum = np.sum(
            np.sum(np.bitwise_and(chi_1_arr, self.chi_1_arr), axis=2), axis=1)
        # chi_2_sum = np.sum(
        #     np.sum(np.bitwise_and(chi_2_arr, self.chi_2_arr), axis=2), axis=1)
        op_sum = np.sum(
            np.sum(np.bitwise_and(op_arr, self.op_arr), axis=2), axis=1)
        op_sum[1] += 1   # 区分减号和加号
        chi_3_sum = np.sum(
            np.sum(np.bitwise_and(chi_3_arr, self.chi_3_arr), axis=2), axis=1)
        num1 = chi_1_sum.argmax()
        # num2 = chi_2_sum.argmax()
        op = op_sum.argmax()
        num3 = chi_3_sum.argmax()
        result = self._cal_result(num1,num3, op)
        print (result)


def test(path):
    crack = PatentCrack('Patent.pkl')

    crack.feed(os.path.join(path))
    # fn_list = [fn for fn in os.listdir(u'../04_data/企业证书/cnca')]
    # fn_list.sort()
    # for fn in fn_list[:50]:
    #     crack.feed(os.path.join(u'../04_data/企业证书/cnca', fn))


# if __name__=='__main__':
#     test()