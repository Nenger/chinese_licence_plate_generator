import cv2
import os
import sys


data_dir = "/img/"

def trans_chinese():
    current_path = sys.path[0]

    img = cv2.imread(current_path + data_dir + "raw/word.png", -1)
    index = 0
    x_step = 90
    y_step = 179

    #第一排
    start_y = 0
    end_y = start_y + y_step
    for i in range(0, 9):
        roi = img[start_y:end_y, i*x_step:(i+1)*x_step]
        cv2.imwrite(current_path + data_dir + "chinese/%02d.png"%(index,), roi)
        index += 1

    #第2排
    start_y += y_step
    end_y = start_y + y_step
    for i in range(0, 9):
        roi = img[start_y:end_y, i*x_step:(i+1)*x_step]
        cv2.imwrite(current_path + data_dir + "chinese/%02d.png"%(index,), roi)
        index += 1

    #第3排
    start_y +=  y_step
    end_y = start_y + y_step
    for i in range(0, 9):
        roi = img[start_y:end_y, i*x_step:(i+1)*x_step]
        cv2.imwrite(current_path + data_dir + "chinese/%02d.png"%(index,), roi)
        index += 1

    #第4排
    start_y +=  y_step
    end_y = start_y + y_step
    for i in range(0, 6):
        roi = img[start_y:end_y, i*x_step:(i+1)*x_step]
        cv2.imwrite(current_path + data_dir + "chinese/%02d.png"%(index,), roi)
        index += 1

def trans_numbers():
    current_path = sys.path[0]

    img = cv2.imread(current_path + data_dir + "raw/letter.png", -1)
    index = 0
    x_step = 90
    y_step = 179

    #第一排
    start_y = y_step*3
    end_y = start_y + y_step
    for i in range(0, 10):
        roi = img[start_y:end_y, i*x_step:(i+1)*x_step]
        cv2.imwrite(current_path + data_dir + "numbers/%d.png"%((index+1)%10,), roi)
        index += 1

def trans_letters():
    current_path = sys.path[0]
    letter_list = [chr(i) for i in range(97,123)]

    img = cv2.imread(current_path + data_dir + "raw/letter.png", -1)
    index = 0
    x_step = 90
    y_step = 179

    #第一排
    start_y = 0
    end_y = start_y + y_step
    for i in range(0, 10):
        roi = img[start_y:end_y, i*x_step:(i+1)*x_step]
        cv2.imwrite(current_path + data_dir + "letters/%s.png"%(letter_list[index],), roi)
        index += 1

    #第二排
    start_y += y_step
    end_y = start_y + y_step
    for i in range(0, 10):
        roi = img[start_y:end_y, i*x_step:(i+1)*x_step]
        cv2.imwrite(current_path + data_dir + "letters/%s.png"%(letter_list[index],), roi)
        index += 1

    #第三排
    start_y += y_step
    end_y = start_y + y_step
    for i in range(0, 6):
        roi = img[start_y:end_y, i*x_step:(i+1)*x_step]
        cv2.imwrite(current_path + data_dir + "letters/%s.png"%(letter_list[index],), roi)
        index += 1

if __name__ == "__main__":
    trans_chinese()
    trans_numbers()
    trans_letters()