import itertools
import math
import os
import random
import sys
import numpy as np
import cv2

#负样本相对于真实车牌, 用于hard negative mining, 来源于测试时出现的误识别目标
#负样本一方面可以进一步降低false positive, 另一方面可以防止模型只学习由于图片叠加式产生的明显边缘
class NegativeObjectGenerator():
    def __init__(self, img_dir, dst_size):
        self.current_path = sys.path[0]

        self.file_path = img_dir
        self.img_dir = img_dir
        self.img_list = os.listdir(self.img_dir)

        #打乱次序
        random.shuffle(self.img_list)

        self.img_num = len(self.img_list)
        self.dst_size = dst_size

        self.current_index = 0
       
    def generate_one_object(self):
            self.current_index += 1
            self.current_index %= self.img_num

            #此时按殊勋读取, 不采取随机选取
            file_name = self.img_list[self.current_index]

            file_full_path = self.img_dir + file_name

            img = cv2.imread(file_full_path)
            img = cv2.resize(img, self.dst_size, interpolation = cv2.INTER_CUBIC)

            return img
