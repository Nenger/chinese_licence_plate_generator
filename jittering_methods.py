import itertools
import math
import os
import random
import sys
import numpy as np
import cv2
import uuid

def jittering_blur(img):
    kernel_list = [3, 5, 7, 11]
    kernel = random.choice(kernel_list)
    sigma = random.uniform(0, 0.8)
    return  cv2.GaussianBlur(img, (kernel,kernel), sigma)   

#随机饱和度, 亮度, 对比度
def jittering_color(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = hsv.astype(np.float64)

    #对hsv进行随机调整, H(色彩/色度)的取值范围是[0,179]，S(饱和度)的取值范围[0,255]，V(亮度)的取值范围[0,255]
    random_h_scale = random.randint(90, 115) / 100.0
    random_s_scale = random.randint(40, 100) / 100.0
    random_v_scale = random.randint(50, 100) / 100.0

    hsv[:,:,0] *= random_h_scale
    hsv[:,:,1] *= random_s_scale
    hsv[:,:,2] *= random_v_scale

    hsv = hsv.astype(np.uint8)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

#随机调整车牌边框
def jittering_border(image): 
    scale_x = random.randint(0, 2)/ 100.0
    scale_y =  random.randint(0, 10)/ 100.0
    height, width = image.shape[:2]
    border_x = int(width * scale_x)
    border_y = int(height * scale_y)

    roi = image[border_y: height - border_y, border_x:width-border_x]
    return roi

def jittering_scale(image):
    h, w = image.shape[:2]

    scale = random.uniform(0.6, 1.0)
    scaled_h = int(h*scale)
    scaled_w = int(w*scale) 
    image = cv2.resize(image, (scaled_w, scaled_h), interpolation = cv2.INTER_CUBIC)
    image = cv2.resize(image, (w, h), interpolation = cv2.INTER_CUBIC)

    return image

