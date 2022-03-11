import sys

import cv2
import glob
import os

path_to_img = glob.glob("C:/Users/chanj/PycharmProjects/demo_airost/02000/*.jpg")
path_to_img2 = glob.glob("C:/Users/chanj/PycharmProjects/demo_airost/03000/*.jpg")
path_to_img3 = glob.glob("C:/Users/chanj/PycharmProjects/demo_airost/00000/*.jpg")
path_to_img4 = glob.glob("C:/Users/chanj/PycharmProjects/demo_airost/01000/*.jpg")
a = path_to_img + path_to_img2 + path_to_img3 + path_to_img4
count = 0
for i in a:
    img = cv2.imread(i)
    img = img[137:887, 137:887]
    img = cv2.resize(img, (224,224))
    cv2.imwrite("mask_weared_incorrect/mask_weared_incorrect{}.png".format(count), img)
    count += 1

