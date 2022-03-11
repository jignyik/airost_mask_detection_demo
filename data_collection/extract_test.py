import sys

train = ["mask_weared_incorrect", "with_mask", 'without_mask']

import shutil, random, os
dirpath = [os.path.join(r"C:\Users\chanj\PycharmProjects\demo_airost\demo_airost\Train", i) for i in train]
destDirectory = [os.path.join(r"C:\Users\chanj\PycharmProjects\demo_airost\demo_airost\Test", i) for i in train]

for o, i in enumerate(dirpath):
    filenames = random.sample(os.listdir(i), 800)
    for fname in filenames:
        srcpath = os.path.join(i, fname)
        des = os.path.join(destDirectory[o], fname)
        print(srcpath)
        print(des)
        shutil.move(srcpath, des)