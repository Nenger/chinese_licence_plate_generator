import itertools
import math
import os
import random
import sys
import numpy as np
import cv2

class RealPlateGenerator():
    def __init__(self, img_dir, dst_size):
        self.current_path = sys.path[0]

        self.file_path = img_dir
        self.img_dir = img_dir
        self.img_list = os.listdir(self.img_dir)

        random.shuffle(self.img_list)

        self.img_num = len(self.img_list)
        self.dst_size = dst_size

        self.current_index = 0

        #map chinese character to a index
        self.chinese_map = {}
        with open(self.current_path + "\chinese_map.txt", 'rb') as f:
            lines = f.readlines()
            first = True
            for line in lines:
                if first:
                    #第一行忽略
                    first = False
                    continue
                else:
                    data = line.decode('utf-8')
                    self.chinese_map[data[0]] = data[3:5]  #!!!!
       
    def generate_one_plate(self):
        while(True):
            self.current_index += 1
            self.current_index %= self.img_num

            #此时按殊勋读取, 不采取随机选取
            file_name = self.img_list[self.current_index]

            if len(file_name) != 11:
                continue

            file_full_path = self.img_dir + file_name

            img = cv2.imdecode(np.fromfile(file_full_path, dtype=np.uint8), -1)
            img = cv2.resize(img, self.dst_size, interpolation = cv2.INTER_CUBIC)
            
            #中文名转换为对应的index
            key = file_name[0]
            name = self.chinese_map[key] + file_name[1:-4]

            return img, name
