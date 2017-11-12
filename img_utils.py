import itertools
import math
import os
import random
import sys
import numpy as np
import cv2
import uuid
import shutil
import time

def reset_folder(path):
     try:
         shutil.rmtree(path)
     except:
          pass
    
     time.sleep(1)     
     
     try:
         os.mkdir(path)
     except:
          pass

#图像添加噪声
def add_noise(img, strenth = 4):
    #需转换为浮点数才能完成除法
    out = img.astype(np.float64)
    out /= 255.0

    #随机添加噪音, 并去掉超过范围的噪音值
    noise_scale = random.randint(0, strenth)/100.0
    out += np.random.normal(scale=noise_scale, size=out.shape)
    out = np.clip(out, 0., 1.)

    out*=255

    out = out.astype(np.uint8)

    return out

#叠加rgba图添加到背景中
def overlay_img(fg, bg, mask, x, y):
    h_fg, w_fg = fg.shape[:2]

    end_x = x + w_fg
    end_y = y + h_fg

    roi = bg[y:end_y, x:end_x]

    #求得logo的二值图和反二值图
    mask_inv = cv2.bitwise_not(mask)

    # 将透明的那部分, 用背景填充
    # Now black-out the area of logo in ROI
    img1_bg = cv2.bitwise_and(roi, roi, mask = mask_inv) ##
    #将前景logo部分,从logoimage中取出, 而其他部分值为0
    # Take only region of logo from logo image.
    img2_fg = cv2.bitwise_and(fg, fg, mask = mask)

    # Put logo in ROI and modify the main image
    try:
       dst = cv2.add(img1_bg, img2_fg)
    except:
       pass

    bg[y:end_y, x:end_x] = dst
    return bg

def euler_to_mat(yaw, pitch, roll):
    # Rotate clockwise about the Y-axis
    c, s = math.cos(yaw), math.sin(yaw)
    M = np.matrix([[  c, 0.,  s],
                    [ 0., 1., 0.],
                    [ -s, 0.,  c]])

    # Rotate clockwise about the X-axis
    c, s = math.cos(pitch), math.sin(pitch)
    M = np.matrix([[ 1., 0., 0.],
                    [ 0.,  c, -s],
                    [ 0.,  s,  c]]) * M

    # Rotate clockwise about the Z-axis
    c, s = math.cos(roll), math.sin(roll)
    M = np.matrix([[  c, -s, 0.],
                    [  s,  c, 0.],
                    [ 0., 0., 1.]]) * M

    return M

#涉及尺度和姿态, 关乎样本的覆盖率
#使用透视变换才是更合理的方案
def make_affine_transform(from_shape, to_shape, 
                        min_scale, max_scale,
                        rotation_variation=1.0,
                        translation_variation=1.0):
    from_size = np.array([[from_shape[1], from_shape[0]]]).T
    to_size = np.array([[to_shape[1], to_shape[0]]]).T

    M = None
    while True:
        #uniform() 方法将随机生成下一个实数，它在 [x, y) 范围内。
        #生成一个随机scale 
        scale = random.uniform(min_scale, max_scale)
                            
        #三个轴的随机旋转, 数值对应弧度
        roll =  random.uniform(-0.2, 0.2) * rotation_variation      #绕着车牌中心旋转
        pitch = random.uniform(-0.7, 0.7) * rotation_variation     #沿着水平中轴翻转
        yaw =   random.uniform(-0.3, 0.3) * rotation_variation     #沿着树脂中走翻转

        # Compute a bounding box on the skewed input image (`from_shape`).
        M = euler_to_mat(yaw, pitch, roll)[:2, :2]
        h, w = from_shape[:2]
        corners = np.matrix([[-w, +w, -w, +w],
                                [-h, -h, +h, +h]]) * 0.5
        skewed_size = np.array(np.max(M * corners, axis=1) -
                                np.min(M * corners, axis=1))

        # Set the scale as large as possible such that the skewed and scaled shape
        # is less than or equal to the desired ratio in either dimension.
        scale *= np.min(to_size / skewed_size)

        # Set the translation such that the skewed and scaled image falls within the output shape bounds
        trans = (np.random.random((2,1)) - 0.5) * translation_variation
        trans = ((2.0 * trans) ** 5.0) / 2.0
        if np.any(trans < -0.5) or np.any(trans > 0.5):
            continue
        trans = (to_size - skewed_size * scale) * trans

        center_to = to_size / 2.
        center_from = from_size / 2.

        M = euler_to_mat(yaw, pitch, roll)[:2, :2]
        M *= scale
        M = np.hstack([M, trans + center_to - M * center_from])

        break

    return M

def save_random_img(dir, img):
    name = dir + str(uuid.uuid1()) + ".png"
    cv2.imwrite(name, img)