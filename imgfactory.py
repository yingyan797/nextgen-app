from PIL import Image, ImageDraw
import numpy as np
import os
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
    pfx = "static/imggroups/"+group_name+'/'
    imgs = os.listdir(pfx)
    if not imgs:
        return
    avgrat = 0
    for i in imgs:
        im = Image.open(pfx+i)
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
    wd = usz[1]+20
    ht = usz[0]+20
    img_template = np.zeros((wd*rownum, ht*colnum, 3), dtype=np.uint8)
    i = 0
    for c in range(colnum):
        for r in range(rownum):
            if i >= len(imgs):
                img_template[c*wd:c*wd+usz[1], r*ht:r*ht+usz[0]] = 155
            else:
                im = Image.open(pfx+imgs[i]).resize(usz)
                img_template[c*wd:c*wd+usz[1], r*ht:r*ht+usz[0]] = np.array(im)[:,:,:3] 
            i += 1
    # mask = Image.new(mode="1", size=im_base.size)
    Image.fromarray(img_template).save("static/result/all.png")
    return imgs, colnum, rownum

def crop_multiple(img_name, instr):
    im = Image.open("static/imgorig/"+img_name)
    res = [] 
    i = 0
    imannot = im.copy()
    annot = ImageDraw.Draw(imannot)
    pfx = "static/result/"+img_name[:-4]
    w, h = im.size
    lw = int(w/200+5)
    for pr in Parser(instr).crop_info():
        wrange = w*pr[:2]
        hrange = h*pr[2:]
        annot.line([(wrange[0], hrange[0]),(wrange[1], hrange[0]),(wrange[1], hrange[1]),(wrange[0], hrange[1]),(wrange[0], hrange[0])], fill="red", width=lw)
        imcr = im.crop((wrange[0], hrange[0], wrange[1], hrange[1]))
        fn = pfx+"(c"+str(i)+").png"
        res.append(fn)
        imcr.save(fn)
        i += 1
    annotfile = pfx+"(annot).png"
    imannot.save(annotfile)
    return [annotfile]+res

def select_multiple(imgs, cols, instr):
    res = []
    for num in Parser(instr).select_info(cols):
        i = int(num)
        if i > len(imgs):
            break
        res.append(imgs[i-1])
    return res

def all_imggroups():
    pfx = "static/imggroups/"
    gs = os.listdir(pfx)
    groups = [("", "Not selected, 0")]
    for g in gs:
        groups.append((g, len(os.listdir(pfx+g))))
    return groups

def find_imggroup(gname):
    f = open("static/imggroups.txt", "r")
    name = True
    while True:
        line = f.readline()
        if not line:
            return False, ""
        if name:
            if line[:-1] == gname:
                return True, f.readline()[:-1]
        name = not name

def remove_nl(desc):
    res = ""
    for c in desc:
        if c == '\n' or c == '\r':
            res += ' '
        else:
            res += c
    return res

def reg_imggroup(gname, desc, exist=True):
    if find_imggroup(gname)[0]:
        return False
    f = open("static/imggroups.txt", "a")
    f.write(gname+'\n'+remove_nl(desc)+'\n')
    if not exist:
        os.mkdir("static/imggroups/"+gname)
    return True

def update_imggroup(gfrom, gto, gdesc, action):
    pfx = "static/imggroups/"
    if action[:5] == "Clear":
        for f in os.listdir(pfx):
            os.remove(pfx+f)
        open("static/imggroups.txt", "w").write("")
        return
    if gfrom:
        if action[:6] == "Delete":
            for f in os.listdir(pfx+gfrom):
                os.remove(pfx+gfrom+f)
        else:
            f = open("static/imggroups.txt", "r")
            lines = f.readlines()
            loc = -1
            for i in range(0, len(lines), 2):
                if lines[i][:-1] == gfrom:
                    loc = i
                    break
            if loc >= 0:
                if action[:6] == "Remove":
                    os.rmdir(pfx+gfrom)
                    lines.pop(loc)
                    lines.pop(loc+1)
                elif action[:7] == "Confirm":
                    if gto:
                        os.rename(pfx+gfrom, pfx+gto)
                        lines[loc] = gto+'\n'
                    if gdesc:
                        lines[loc+1] = gdesc+'\n'
                f = open("static/imggroups.txt", "w")
                f.writelines(lines)

def update_airesult(action):
    pfx = "static/result/"
    if action[:5] == "Clear":
        for f in os.listdir(pfx):
            os.remove(pfx+f)

# crop_multiple("cube.png", "width 51% to 100%, height 0% to 100%")
# img_combine("graphics")

