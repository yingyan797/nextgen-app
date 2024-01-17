from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os, glob
from answer_parser import Parser

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
    pfx = "static/imggroups/"
    imgs = os.listdir(pfx+group_name)
    if not imgs:
        return
    avgrat = 0
    for i in imgs:
        im = Image.open(pfx+group_name+i)
        w, h = im.size
        avgrat += w/h
    avgrat /= len(imgs)
    usz = int(120*avgrat), 120
    if avgrat < 1:
        usz = 120, int(120/avgrat)
    colnum = int(np.ceil(np.sqrt(len(imgs))))
    rownum = colnum-1
    if rownum*colnum < len(imgs):
        rownum += 1
    wd = usz[1]+10
    ht = usz[0]+10
    img_template = np.zeros((wd*rownum, ht*colnum, 3), dtype=np.uint8)
    i = 0
    for c in range(colnum):
        for r in range(rownum):
            im = Image.open(pfx+group_name+imgs[i]).resize(usz)
            img_template[c*wd:c*wd+usz[1], r*ht:r*ht+usz[0]] = im
            i += 1
    # mask = Image.new(mode="1", size=im_base.size)
    Image.fromarray(img_template).save(pfx+"all.png")
    return imgs

def crop_multiple(img_name, instr):
    im = Image.open("static/imgorig/"+img_name)
    res = [] 
    i = 0
    for pr in Parser(instr).crop_info():
        w, h = im.size
        wrange = w*pr[:2]
        hrange = h*pr[2:]
        imcr = im.crop((wrange[0], hrange[0], wrange[1], hrange[1]))
        fn = "static/ai_crop/"+img_name[:-4]+"(c"+str(i)+").png"
        res.append(fn)
        imcr.save(fn)
        i += 1
    return res

def all_imggroups():
    pfx = "static/imggroups/"
    gs = os.listdir(pfx)
    groups = []
    for g in gs:
        groups.append((g, len(os.listdir(pfx+g))))
    return groups

def update_imggroups(gfrom, gto, action):
    if action[:5] == "Clear":
        for f in os.listdir(pfx):
            os.remove(pfx+f)
        return
    pfx = "static/imggroups/"
    if gfrom:
        if action[:6] == "Remove":
            os.rmdir(pfx+gfrom)
        elif action[:6] == "Delete":
            for f in os.listdir(pfx+gfrom):
                os.remove(pfx+gfrom+f)
        elif action[:6] == "Rename" and gto:
            os.rename(pfx+gfrom, pfx+gto)
    if gto and action[:6] == "Create":
        os.mkdir(pfx+gto)

def update_aicrop(action):
    pfx = "static/ai_crop/"
    if action[:5] == "Clear":
        for f in os.listdir(pfx):
            os.remove(pfx+f)

# crop_multiple("static/dhabi.png", "To crop the image to focus on Al Lulu Island while maintaining the context of its location, you might consider the following percentage ranges: Width: 10% to 45%, Height: 5% to 50%, These ranges should help you")
# img_combine("graphics")

