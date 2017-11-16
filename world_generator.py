import itertools
import math
import os
import random
import sys
import numpy as np
import cv2

#get some random background image based on a opensource dataset
class  WorldGenerator():
    def __init__(self, img_dir, empty_dir, world_size):
        self.output_shape = world_size
        self.img_dir = img_dir
        self.img_list = os.listdir(self.img_dir)

        random.shuffle(self.img_list)
        self.img_num = len(self.img_list)

        #empty world
        self.empty_world = cv2.imread(empty_dir + "blue.bmp")
        self.empty_world = cv2.resize(self.empty_world, self.output_shape, interpolation = cv2.INTER_AREA)
        
    #empth world means the background color is the same as the plate color 
    def generator_empty_world(self, color = 1):
        return self.empty_world.copy()

    def generate_one_world(self):
        current_path = sys.path[0]

        while True:
            index = random.randint(0, self.img_num  - 1)
            fname = self.img_dir + self.img_list[index]

            img = cv2.imread(fname, -1)

            #we do not use one channnel image
            if (len(img.shape) > 2 and  img.shape[1] >= self.output_shape[0] and img.shape[0] >= self.output_shape[1]):
                break

        #get a roi with random position from the raw image
        x = random.randint(0, img.shape[1] - self.output_shape[0])
        y = random.randint(0, img.shape[0] - self.output_shape[1])
        img = img[y:y + self.output_shape[1], x:x + self.output_shape[0]]

        return img
