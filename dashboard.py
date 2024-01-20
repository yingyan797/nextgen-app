from flask import Flask, render_template, request
import models as mo
import imgfactory as imf

app = Flask(__name__)

@app.route('/sample', methods=['GET', 'POST'])    # main page
def sample():
    prompt = request.form.get('prompt')
    print(request.form)
    res = 0 # image 1 answer 2 audio 3
    ans = ""
    image_url = ""
    fn = ""
    if prompt:
        fn = request.form.get("fn")
        if request.form.get('image_gen'):
            if not fn:
                fn = "imggen"
            mo.image_gen(prompt=prompt, fn=fn)
            res = 1
        elif request.form.get('ask'):
            img = request.form.get('img')
            if img:
                image_url = "static/imgorig/"+img
            mtoken = request.form.get("mtoken")
            if mtoken:
                mtoken = int(mtoken)
            else:
                mtoken = 250
            ans = mo.answer(prompt=prompt, image_url=image_url, mtoken=mtoken)
            res = 2
        elif request.form.get('tts'):
            if not fn:
                fn = "speech"
            mo.text_speech(text=prompt, fn=fn)
            res = 3
    return render_template('sample.html', image_url=image_url, prompt=prompt, fn=fn, result=res, answer=ans)

@app.route('/', methods=['GET', 'POST'])    # main page
def index():
    print(request.form)
    imgcrop = request.form.get("imgcrop")
    group = request.form.get("groupt")
    if not group:
        group = request.form.get("groupd")
    crops = []
    findorig = []
    expl = ""
    if imgcrop:
        w,h = imf.Image.open("static/imgorig/"+imgcrop).size
        desc = request.form.get("cropdesc")
        if desc:
            objnum = request.form.get("num")
            numdesc = ". "
            mxtk = 75
            match objnum:
                case "1": 
                    numdesc += "Only one"
                    mxtk += 50
                case "s": 
                    numdesc += "About 2 to 4"
                    mxtk += 180
                case "m": 
                    numdesc += "About 5 to 10"
                    mxtk += 400
                case "l": 
                    numdesc += "A large number of (over 10)"
                    mxtk += 800
                case _: numdesc += "Not sure how many"
            numdesc += " objects in total is expected to be cropped."
            prompt = "Please find the following object(s) from the image (size "+str(w)+'*'+str(h)+"): "
            prompt += desc+numdesc+" For each one, answer how to crop by giving the percentage ranges on width and height, format: width a% to b%, height c% to d%. Try to keep the whole object."
            print(prompt)
            pfx = "static/imgorig/"
            expl = desc+"\n\n"+mo.answer(prompt=prompt, image_url=pfx+imgcrop, mtoken=mxtk)
            crops = imf.crop_multiple(imgcrop, expl)
    elif group:
        imgs,c,r = imf.img_combine(group)
        imgdesc = request.form.get("imgdesc")
        f, gdesc = imf.find_imggroup(group)
        if gdesc:
            gdesc = ". All small pictures have common features: "+gdesc
        prompt = "This is a "+str(r)+'*'+str(c)+" grid of small pictures, each has an index on the top left"+gdesc+". Select the indexes of pictures best matching the following descriptions: "+imgdesc+". Answer format: Number a, Number b... Explain the selection."
        expl = imgdesc+gdesc+"\n\n"+mo.answer(prompt=prompt, image_url="static/result/all.png", mtoken=100)
        findorig = ["static/imggroups/"+group+"/"+res for res in imf.select_multiple(imgs, expl)]
        findorig.append("static/result/all.png")

    groups = imf.all_imggroups()
    return render_template('index.html', groups=groups, crops=crops, findorig=findorig, expl=expl)

@app.route('/imggroups', methods=['GET', 'POST'])    # main page
def imggroups():
    print(request.form)
    action = request.form.get("action")
    pre = request.form.get("pre")
    if pre:
        action = pre
    group = request.form.get("groupt")
    if not group:
        group = request.form.get("groupd")
    if not group:
        group = request.form.get("gname")
    
    gname = group
    desc = ""
    allclasses = []
    created = 3
    ask = False
    if action:
        newgroup = request.form.get("groupn")
        gdesc = request.form.get("desc")
        if action[:4] == "View":
            gname = group
            found, d = imf.find_imggroup(group)
            if not found:
                gname = "**image class not exist**"
            else:
                desc = d        
            
        elif action[:6] == "Create":
            if newgroup:
                if imf.reg_imggroup(newgroup, gdesc):
                    created = 1
                else:
                    created = 0
        elif action[:7] != "Confirm":
            if request.form.get("Yes"):
                imf.update_imggroup(group, newgroup, gdesc, action)
            elif request.form.get("No") is None:
                ask = True
        else:
            imf.update_imggroup(group, newgroup, gdesc, action)
            created = 2
    
    elif request.form.get("allclasses"):
        allclasses = imf.imggroups_nd()
    
    groups = imf.all_imggroups()
    return render_template('imggroups.html', gname=gname, desc=desc, groups=groups, 
                           allclasses=allclasses, ask=ask, action=action, created=created)
            

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)