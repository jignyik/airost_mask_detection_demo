import glob
import sys

import cv2

a = glob.glob('C:/Users/chanj/PycharmProjects/demo_airost/lfw/*/*.jpg')
print(a)

count = 1
for i in a:
    img = cv2.imread(i)
    img = img[63:187, 63:187]
    img = cv2.resize(img, (224, 224))
    cv2.imwrite("without_mask/without_mask{}.png".format(count), img)
    count += 1
    if count == 2300:
        sys.exit()