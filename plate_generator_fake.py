import itertools
import math
import os
import random
import sys
import numpy as np
import cv2

from img_utils import *

class FakePlateGenerator():
    def __init__(self, fake_resource_dir, plate_size):
        chinese_dir = fake_resource_dir + "/chinese/"
        number_dir = fake_resource_dir + "/numbers/" 
        letter_dir = fake_resource_dir + "/letters/" 
        plate_dir = fake_resource_dir + "/plate_background_use/"

         #缩放是通过控制y方向的像素值, 因为各个个字符宽度是不同的(比如I的宽度就很小)
        character_y_size = 113
        plate_y_size = 164

        self.dst_size = plate_size

        self.chinese = self.load_image(chinese_dir, character_y_size)
        self.numbers = self.load_image(number_dir, character_y_size)
        self.letters = self.load_image(letter_dir, character_y_size)

        #合并字典
        self.numbers_and_letters = dict(self.numbers, **self.letters)

        #为简化工作,当前只使用蓝牌,如果要加入其他颜色牌照,文字颜色需调整
        self.plates = self.load_image(plate_dir, plate_y_size)
    
        #车牌背景转换为RGBA便于与RGBA格式的图片叠加
        for i in self.plates.keys():
            self.plates[i] = cv2.cvtColor(self.plates[i], cv2.COLOR_BGR2BGRA)

        #每个字符在车牌中的x坐标
        self.character_position_x_list_part_1 = [43, 111]                   #"苏A" 这两个字符
        self.character_position_x_list_part_2 = [205, 269, 330, 395, 464]   #后面的五个字符
    
    def get_radom_sample(self, data):
        keys = list(data.keys())
        i = random.randint(0, len(data) - 1)
        key = keys[i]
        value = data[key]

        #注意对矩阵的深拷贝
        return key, value.copy()

    def load_image(self, path, dst_y_size):
        img_list = {}
        current_path = sys.path[0]

        listfile = os.listdir(path)     

        for filename in listfile:
            img = cv2.imread(path + filename, -1)
            
            height, width = img.shape[:2]
            x_size = int(width*(dst_y_size/height))
            img_scaled = cv2.resize(img, (x_size, dst_y_size), interpolation = cv2.INTER_CUBIC)
            
            img_list[filename[:-4]] = img_scaled

        return img_list

    def add_character_to_plate(self, character, plate, x):
        h_plate, w_plate = plate.shape[:2]
        h_character, w_character = character.shape[:2]

        start_x = x - int(w_character/2)
        start_y = int((h_plate - h_character)/2)

        a_channel = cv2.split(character)[3]
        ret, mask = cv2.threshold(a_channel, 100, 255, cv2.THRESH_BINARY)

        overlay_img(character, plate, mask, start_x, start_y)

    def generate_one_plate(self):
        _, plate_img = self.get_radom_sample(self.plates)
        plate_name = ""
    
        character, img = self.get_radom_sample(self.chinese)
        self.add_character_to_plate(img, plate_img, self.character_position_x_list_part_1[0])
        plate_name += "%s"%(character,)

        character, img = self.get_radom_sample(self.letters)
        self.add_character_to_plate(img, plate_img, self.character_position_x_list_part_1[1])
        plate_name += "%s"%(character,)

        for i in range(5):
            character, img =  self.get_radom_sample(self.numbers_and_letters)
            self.add_character_to_plate(img, plate_img, self.character_position_x_list_part_2[i])
            plate_name += character

        #转换为RBG三通道
        plate_img = cv2.cvtColor(plate_img, cv2.COLOR_BGRA2BGR)

         #转换到目标大小
        plate_img = cv2.resize(plate_img, self.dst_size, interpolation = cv2.INTER_CUBIC)

        return plate_img, plate_name
