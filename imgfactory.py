from PIL import Image
import numpy as np
import os
from matplotlib import pyplot as plt

def create_samples(group_name):
    img_template = np.zeros((100,100,3), dtype=np.uint8)
    colors = np.array([[150,0,0],[0,150,0],[0,0,150],[100,100,100]])
    i = 0
    for c0 in colors:
        for c1 in colors:
            for c2 in colors:
                for c3 in colors:
                    img_template[0:50,0:50] = c0
                    img_template[0:50,50:] = c1
                    img_template[50:,0:50] = c2
                    img_template[50:,50:] = c3
                    im = Image.fromarray(img_template)
                    im.save("static/"+group_name+'/'+str(i)+".png")
                    i += 1

def img_combine(group_name):
    f = open("static/imggroups.csv", "r")
    num = 0
    while True:
        line = f.readline()
        if not line:
            break
        info = line[:-1].split(",")
        if info[0] == group_name:
            num = int(info[1])
    avgrat = 0
    for i in range(num):
        im = Image.open("static/"+group_name+'/'+str(i)+".png")
        w, h = im.size
        avgrat += w/h
    avgrat /= num
    usz = int(120*avgrat), 120
    if avgrat < 1:
        usz = 120, int(120/avgrat)
    colnum = int(np.ceil(np.sqrt(num)))
    rownum = colnum-1
    if rownum*colnum < num:
        rownum += 1
    wd = usz[1]+10
    ht = usz[0]+10
    img_template = np.zeros((wd*rownum, ht*colnum, 3), dtype=np.uint8)
    i = 0
    for c in range(colnum):
        for r in range(rownum):
            im = Image.open("static/"+group_name+'/'+str(i)+".png").resize(usz)
            img_template[c*wd:c*wd+usz[1], r*ht:r*ht+usz[0]] = im
            i += 1
    Image.fromarray(img_template).save("static/"+group_name+"/all.png")

# im = Image.open("static/southquay.jpg")
# print(np.array(im).shape)
# rsim = im.resize((200,50))
# rsim.save("static/sqrs.jpg")
