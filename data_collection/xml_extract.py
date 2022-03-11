import sys

import numpy as np
from lxml import etree
from io import StringIO, BytesIO
import cv2
import glob
import os
import shutil

file = ["mask_weared_incorrect", "with_mask", "without_mask"]

for i in file:
    try:
        shutil.rmtree(i)
    except FileNotFoundError:
        pass
for i in file:
    try:
        os.mkdir(i)
    except FileExistsError:
        pass
count = 1
for i in glob.glob("C:/Users/chanj/PycharmProjects/demo_airost/annotations/*.xml"):
    print(i)
    tree = etree.parse(i)
    root = tree.getroot()

    filename = [i.text for i in root.iter('filename')]
    name = [i.text for i in root.iter('name')]
    bndbox = [[]]
    boxes = []
    box = ['xmin', 'ymin', 'xmax', 'ymax']
    coor = []
    for o in root.iter(z for z in box):
        coor.append(o.text)
        if len(coor) == 4:
            boxes.append(coor)
            coor = []

    boxes = np.array(boxes).astype("float32")
    path = r"images"
    img = cv2.imread(os.path.join(path, filename[0]))
    for o,i in enumerate(boxes):
        xdiff = i[2] - i[0]
        ydiff = i[3] - i[1]
        if xdiff < ydiff:
            diffneed = ydiff-xdiff
            i[0] -= diffneed/2
            i[2] += diffneed/2
        else:
            diffneed = xdiff - ydiff
            i[1] -= diffneed / 2
            i[3] += diffneed / 2
        i = i.astype('int')
        crop_img = img[i[1]:i[3], i[0]:i[2]]
        if crop_img.any():
            crop_img = cv2.resize(crop_img, (224, 224))
            cv2.imwrite("{}/{}{}.png".format(name[o], filename[0], count), crop_img)
            count += 1
