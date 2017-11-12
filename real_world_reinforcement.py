import itertools
import math
import os
import random
import sys
import numpy as np

import cv2
import numpy

class  RealWorldReinforcement():
    def __init__(self, img_dir, dst_size):
        self.dst_size = dst_size
        self.img_dir = img_dir
        self.img_list = os.listdir(self.img_dir)

        #打乱次序
        random.shuffle(self.img_list)
        self.img_num = len(self.img_list)
        self.current_index = 0

    def generate_one_world(self):
        current_path = sys.path[0]

        img_name = self.img_dir + self.img_list[self.current_index]
        self.current_index = (self.current_index + 1) % self.img_num

        img = cv2.imread(img_name)

        #解析位置
        p = 9
        x_s = img_name[p:p + 4]
        p += 5
        y_s = img_name[p:p + 4]
        p += 5
        width_s = img_name[p:p + 4]
        p += 5
        height_s = img_name[p:p + 4]
        p += 5
        
        plate_x = int(x_s)
        plate_y = int(y_s)
        plate_width = int(width_s)
        plate_height = int(height_s)

        scale = 0.2

        x_begin = random.randint(0, int(plate_x*scale))
        x_end = random.randint(plate_x, img.shape[1] - self.output_shape[0])
        y_begin = 
        y_end = 
        y = random.randint(0, img.shape[0] - self.output_shape[1])
        img = img[y:y + self.output_shape[1], x:x + self.output_shape[0]]


        #颜色

        #尺度

        #透视
        #很麻烦

        #噪音

        #模糊

        return img


if __name__ == "__main__":
