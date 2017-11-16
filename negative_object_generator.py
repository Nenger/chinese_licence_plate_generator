import itertools
import math
import os
import random
import sys
import numpy as np
import cv2

#negative objects is for hard negative mining
class NegativeObjectGenerator():
    def __init__(self, img_dir, dst_size):
        self.current_path = sys.path[0]

        self.file_path = img_dir
        self.img_dir = img_dir
        self.img_list = os.listdir(self.img_dir)

        random.shuffle(self.img_list)

        self.img_num = len(self.img_list)
        self.dst_size = dst_size

        self.current_index = 0
       
    def generate_one_object(self):
            self.current_index += 1
            self.current_index %= self.img_num

            file_name = self.img_list[self.current_index]

            file_full_path = self.img_dir + file_name

            img = cv2.imread(file_full_path)
            img = cv2.resize(img, self.dst_size, interpolation = cv2.INTER_CUBIC)

            return img
