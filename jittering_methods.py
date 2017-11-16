import itertools
import math
import os
import random
import sys
import numpy as np
import cv2
import uuid

def jittering_blur(img, max_sigma = 0.8):
    kernel_list = [3, 5, 7, 11]
    kernel = random.choice(kernel_list)
    sigma = random.uniform(0, max_sigma)
    return  cv2.GaussianBlur(img, (kernel,kernel), sigma)   

def jittering_color(img, h1 = 90, h2 = 115, s1 = 40, s2 = 100, v1 = 50, v2 = 100):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = hsv.astype(np.float64)

    random_h_scale = random.randint(h1, h2) / 100.0
    random_s_scale = random.randint(s1, s2) / 100.0
    random_v_scale = random.randint(v1, v2) / 100.0

    hsv[:,:,0] *= random_h_scale
    hsv[:,:,1] *= random_s_scale
    hsv[:,:,2] *= random_v_scale

    hsv = hsv.astype(np.uint8)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def jittering_border(image, max_x_percent = 2, max_y_percent = 10): 
    scale_x = random.randint(0, max_x_percent)/ 100.0
    scale_y =  random.randint(0, max_y_percent)/ 100.0
    height, width = image.shape[:2]
    border_x = int(width * scale_x)
    border_y = int(height * scale_y)

    roi = image[border_y: height - border_y, border_x:width-border_x]
    return roi

def jittering_scale(image, min_scale = 0.5, max_scale = 1.0):
    h, w = image.shape[:2]

    scale = random.uniform(min_scale, max_scale)
    scaled_h = int(h*scale)
    scaled_w = int(w*scale) 

    image = cv2.resize(image, (scaled_w, scaled_h), interpolation = cv2.INTER_CUBIC)
    image = cv2.resize(image, (w, h), interpolation = cv2.INTER_CUBIC)

    return image

