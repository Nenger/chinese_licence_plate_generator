import itertools
import math
import os
import random
import sys
import numpy as np
import cv2

from fake_plate_generator import *
from real_plate_generator import *
from img_utils import *
from world_generator import *
from jittering_methods import *
from negative_object_generator import*

#add an object to the world(background)
def add_object_to_world(object, world, min_scale, max_scale):
    dis_height = object.shape[0]*4
    dst_width =  object.shape[1]*2

    M = make_affine_transform( from_shape=object.shape,
                                to_shape=(dis_height, dst_width),
                                min_scale=min_scale,
                                max_scale=max_scale)

    object_mask =  np.ones(object.shape[:2], dtype=np.uint8)*255                       

    object = cv2.warpAffine(object, M, (dst_width, dis_height))
    object_mask = cv2.warpAffine(object_mask, M, (dst_width, dis_height))

    #set all the pixels to 0 or 1
    ret, object_mask = cv2.threshold(object_mask, 253, 255, cv2.THRESH_BINARY)  
    (p_x, p_y, p_w, p_h) = cv2.boundingRect(object_mask)

    #get a random position to put the object in
    x = random.randint(0, world.shape[1] - object.shape[1])
    y = random.randint(0, world.shape[0] - object.shape[0])

    object_in_world = overlay_img(object, world, object_mask, x, y)

    return object_in_world,  (x + p_x, y + p_y, p_w, p_h)

def generate_img_set(output_dir, need_img_num,  real_resource_dir, world_resource_dir, negative_resource_dir):
    current_path = sys.path[0]

    #the image size and plate size we wanted
    world_size = (540, 320)
    plate_size = (100, 30)

    #get plate size in random scale
    min_scale = 0.3
    max_scale = 0.8

    fake_resource_dir  = current_path + "/fake_resource/" 
    empty_world_dir = current_path + "/empty_world/"
    output_world_dir = output_dir

    fake_plate_generator = FakePlateGenerator(fake_resource_dir, plate_size)
    real_plate_generator = RealPlateGenerator(real_resource_dir, plate_size)
    negative_object_generator = NegativeObjectGenerator(negative_resource_dir, plate_size)
    world_generator = WorldGenerator(world_resource_dir, empty_world_dir, world_size)
    
    index = 0
    while index < need_img_num:
        try:
            empty_world = False

            #get a background image, I called it 'world' here
            if index % 30 != 0:
               world = world_generator.generate_one_world()
            else:
               world = world_generator.generator_empty_world()
               empty_world = True

            #add some negative objects to the world
            negative_num = random.randint(0 , 8)
            for i in range(negative_num):
                negative_object = negative_object_generator.generate_one_object()
                negative_object = jittering_color(negative_object)
                negative_object = jittering_blur(negative_object)
                negative_object = jittering_scale(negative_object)
                negative_object = add_noise(negative_object)
                add_object_to_world(negative_object, world, min_scale, max_scale)

            plate = None
            plate_name = ""

            if index % 2 != 0:
                plate, plate_name = real_plate_generator.generate_one_plate()
            else:
                plate, plate_name = fake_plate_generator.generate_one_plate()
                if not empty_world:
                    plate = jittering_color(plate)
                plate = add_noise(plate)
                plate = jittering_blur(plate)
                plate = jittering_scale(plate)
            
            plate = jittering_border(plate)

            #add plate or negative objects to world
            img, coordinate = add_object_to_world(plate, world, min_scale, max_scale)
            img = add_noise(img, 2)

            if empty_world:
                img = jittering_color(img)

            #format output file name
            (x, y, width , height) = coordinate
            location_str = "_%04d_%04d_%04d_%04d"%(x, y, width, height)

            #draw rect for debug
            #plate_in_world = cv2.rectangle(img, (x, y), (x + width, y + height), (0,255,0), 3)

            save_file_name = plate_name + location_str + ".png"
            cv2.imwrite(output_world_dir + save_file_name, img)
        except:
            continue

        index += 1
        print("progress: %04d / %04d"%(index, need_img_num))

if __name__ == "__main__":
    current_path = sys.path[0]

    if 'NENGER_PC' not in os.environ.keys():
        #this is demo environment
        train_set_output_dir = current_path + "/demo_output_train/"
        validation_set_output_dir = current_path + "/demo_output_train/"

        #you need add more images to these folders
        real_resource_dir  = current_path + "/demo_data_sets/real_plate/"
        world_resource_dir = current_path + "/demo_data_sets/SUN397_listed/"
        negative_resource_dir = current_path + "/demo_data_sets/negative_objects/"
    else:
        #ignore this branch, this is my environment
        train_set_output_dir = "E:/plate_detect_data/raw_image/train/"
        validation_set_output_dir = "E:/plate_detect_data/raw_image/validation/"

        real_resource_dir  = "E:/datasets/real_plate/0926-0968/"
        world_resource_dir = "E:/datasets/SUN397_listed/"
        negative_resource_dir = "E:/datasets/negative_objects/" 

    reset_folder(train_set_output_dir)
    reset_folder(validation_set_output_dir)

    generate_img_set(train_set_output_dir, 10000, real_resource_dir, world_resource_dir, negative_resource_dir)
    #generate_img_set(validation_set_output_dir ,3000, real_resource_dir, world_resource_dir, negative_resource_dir)