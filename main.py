import itertools
import math
import os
import random
import sys
import numpy as np
import cv2

from plate_generator_fake import *
from plate_generator_real import *
from img_utils import *
from world_generator import *
from jittering_methods import *

def add_plate_to_world(plate, world, min_scale, max_scale):
    dis_height = plate.shape[0]*4
    dst_width =  plate.shape[1]*2

    M = make_affine_transform( from_shape=plate.shape,
                                to_shape=(dis_height, dst_width),
                                min_scale=min_scale,
                                max_scale=max_scale,
                                rotation_variation=1.0,
                                translation_variation=1.2)

    plate_mask =  np.ones(plate.shape[:2], dtype=np.uint8)*255                           

    #mask是用于与场景融合, 注意这里约束了车牌变换后的尺寸, 需修改  
    plate = cv2.warpAffine(plate, M, (dst_width, dis_height))
    plate_mask = cv2.warpAffine(plate_mask, M, (dst_width, dis_height))

    (p_x, p_y, p_w, p_h) = cv2.boundingRect(plate_mask)

    #随机生成车牌出现在场景中的位置
    x = random.randint(0, world.shape[1] - plate.shape[1])
    y = random.randint(0, world.shape[0] - plate.shape[0])

    out = overlay_img(plate, world, plate_mask, x, y)

    #返回图像和车牌位置
    return out,  (x + p_x, y + p_y, p_w, p_h)

def generate_img_set(output_dir, num):
    current_path = sys.path[0]

    #实际输入的车牌应该与以下参数相当
    world_size = (214, 214)
    plate_size = (60, 21)
    min_scale = 0.7
    max_scale = 1.0

    real_resource_dir  = "D:/datasets/real_plate/0926-0968/"
    world_resource_dir = "D:/datasets/SUN397_listed/"

    need_img_num = num
    fake_resource_dir  = current_path + "/fake_resource/" 
    output_plate_dir = current_path + "/output_plate/"
    output_world_dir = output_dir

    fake_plate_generator = FakePlateGenerator(fake_resource_dir, plate_size)
    real_plate_generator = RealPlateGenerator(real_resource_dir, plate_size)
    world_generator = WorldGenerator(world_resource_dir, world_size)
    
    index = 0
    while index < need_img_num:
        plate = None
        plate_name = ""

        try:
            if index % 2 != 0:
                plate, plate_name = real_plate_generator.generate_one_plate()
            else:
                plate, plate_name = fake_plate_generator.generate_one_plate()
                plate = jittering_color(plate)
                plate = add_noise(plate)
                if index %4 == 0:
                    plate = jittering_blur(plate)
                    plate = jittering_scale(plate)

            plate = jittering_border(plate)
            world = world_generator.generate_one_world()
            
            #车牌放入世界
            img, coordinate = add_plate_to_world(plate, world, min_scale, max_scale)

            #写文件
            (x, y, width , height) = coordinate
            location_str = "_%04d_%04d_%04d_%04d"%(x, y, width , height)

            #画车牌位置框
            #plate_in_world = cv2.rectangle(img, (x, y), (x + width, y + height), (0,255,0), 3)

            save_file_name = plate_name + location_str + ".png"
            #cv2.imwrite(output_plate_dir + save_file_name, plate)
            cv2.imwrite(output_world_dir + save_file_name, img)
        except:
            continue

        index += 1
        print("progress: %04d / %04d"%(index, need_img_num))


if __name__ == "__main__":
    train_set_dir = "E:/plate_detect_data/raw_image/train/"
    validation_set_dir = "E:/plate_detect_data/raw_image/validation/"

    reset_folder(train_set_dir)
    reset_folder(validation_set_dir)

    generate_img_set(train_set_dir, 40000)
    generate_img_set(validation_set_dir ,10000)