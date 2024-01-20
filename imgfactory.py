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
    usz = int(170*avgrat), 170
    if avgrat < 1:
        usz = 170, int(170/avgrat)
    colnum = int(np.ceil(np.sqrt(len(imgs))))
    rownum = colnum-1
    if rownum*colnum < len(imgs):
        rownum += 1
    wd = usz[1]+10
    ht = usz[0]+30
    margin = 15
    img_template = np.zeros((wd*rownum+margin, ht*colnum+margin, 3), dtype=np.uint8)+155
    i = 0
    for c in range(colnum):
        for r in range(rownum):
            if i >= len(imgs):
                img_template[c*wd+margin:c*wd+usz[1]+margin, r*ht+margin:r*ht+usz[0]+margin] = 90
            else:
                im = Image.open(pfx+imgs[i]).resize(usz)
                img_template[c*wd+margin:c*wd+usz[1]+margin, r*ht+margin:r*ht+usz[0]+margin] = np.array(im)[:,:,:3] 
            i += 1
    res = Image.fromarray(img_template)
    dres = ImageDraw.Draw(res)
    i = 1
    for c in range(colnum):
        for r in range(rownum):
            dres.text((r*ht+5,c*wd+5), str(i), fill="green")
            i += 1
    res.save("static/result/all.png")
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
        wrange = w*pr[0], w*pr[1]
        hrange = h*pr[2], h*pr[3]
        annot.line([(wrange[0], hrange[0]),(wrange[1], hrange[0]),(wrange[1], hrange[1]),(wrange[0], hrange[1]),(wrange[0], hrange[0])], fill="red", width=lw)
        imcr = im.crop((wrange[0], hrange[0], wrange[1], hrange[1]))
        fn = pfx+"(c"+str(i)+").png"
        res.append(fn)
        imcr.save(fn)
        i += 1
    annotfile = pfx+"(annot).png"
    imannot.save(annotfile)
    return [annotfile]+res

def select_multiple(imgs, instr):
    res = ([],[])
    for num in Parser(instr).grammar_nums(["Number", "num"]):
        i = int(num)
        if i > len(imgs):
            break
        elif i not in res[0]:
            res[0].append(i)
            res[1].append(imgs[i-1])
    return res[1]

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

def reg_imggroup(gname, desc):
    if find_imggroup(gname)[0]:
        return False
    f = open("static/imggroups.txt", "a")
    f.write(gname+'\n'+remove_nl(desc)+'\n')
    pfx = "static/imggroups/"
    if gname not in os.listdir(pfx):
        os.mkdir(pfx+gname)
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
                    lines.pop(loc)
                elif action[:7] == "Confirm":
                    if gto:
                        os.rename(pfx+gfrom, pfx+gto)
                        lines[loc] = gto+'\n'
                    if gdesc:
                        lines[loc+1] = gdesc+'\n'
                f = open("static/imggroups.txt", "w")
                f.writelines(lines)

def imggroups_nd():
    info = []
    f = open("static/imggroups.txt", "r")
    while True:
        name = f.readline()
        if name:
            desc = f.readline()
            info.append((name[:-1], desc[:-1]))
        else:
            return info

def update_airesult(action):
    pfx = "static/result/"
    if action[:5] == "Clear":
        for f in os.listdir(pfx):
            os.remove(pfx+f)

# crop_multiple("cube.png", "width 51% to 100%, height 0% to 100%")
# img_combine("graphics")

