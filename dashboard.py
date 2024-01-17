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
    dest = request.form.get("dest")
    if not dest:
        dest = ""
    if prompt:
        if request.form.get('image_gen'):
            mo.image_gen(prompt=prompt, dest=dest)
            res = 1
        elif request.form.get('ask'):
            img = request.form.get('img')
            if img:
                image_url = "static/"+img
            mtoken = request.form.get("mtoken")
            if mtoken:
                mtoken = int(mtoken)
            else:
                mtoken = 250
            ans = mo.answer(prompt=prompt, image_url=image_url, mtoken=mtoken, dest=dest)
            res = 2
        elif request.form.get('tts'):
            mo.text_speech(text=prompt, dest=dest)
            res = 3
    print(res)
    return render_template('sample.html', image_url=image_url, prompt=prompt, result=res, answer=ans)

@app.route('/', methods=['GET', 'POST'])    # main page
def index():
    print(request.form)
    action = request.form.get("action")
    if action:
        group = request.form.get("groupt")
        if not group:
            group = request.form.get("groupd")
        newgroup = request.form.get("groupn")
        imf.update_imggroups(group, newgroup, action)
            
    imgcrop = request.form.get("imgcrop")
    res = []
    instr = ""
    if imgcrop:
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
            prompt = "The task is to generate crops of the given image. Please find the following object(s) from the image: "
            prompt += desc+numdesc+" Answer how to crop by giving the percentage ranges on width and height to keep the original image, format is width a% to b%, height c% to d%. Do this for each object to crop."
            print(prompt)
            pfx = "static/imgorig/"
            instr = mo.answer(prompt=prompt, image_url=pfx+imgcrop, mtoken=mxtk)
            crops = imf.crop_multiple(imgcrop, instr)
            for i in range(len(crops)):
                res.append((crops[i], i))
            imgcrop = pfx+imgcrop

    imggroups = imf.all_imggroups()
    print(res)
    return render_template('index.html', imggroups=imggroups, cropannot=imgcrop, crops=res, cropexpl=instr)

@app.route('/cropres', methods=['GET', 'POST'])    # main page
def cropres():
    print(request.form)
    action = request.form.get("action")
    if action:
        imf.update_aicrop(action)
        
    cropannot = request.form.get("cropannot")
    res = []
    i = 0
    while True:
        r = request.form.get("crops"+str(i))
        if r:
            res.append((r,i))
            i += 1
        else:
            break
    return render_template('cropres.html', cropannot=cropannot, res=res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)