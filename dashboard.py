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
    group = request.form.get("groupt")
    if not group:
        group = request.form.get("groupd")
    if group:
        num = 0
        if request.form.get("Remove"):
            num = -1
        imf.imggroup_update(group, num)
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
                    mxtk += 20
                case "s": 
                    numdesc += "About 2 to 4"
                    mxtk += 70
                case "m": 
                    numdesc += "About 5 to 10"
                    mxtk += 150
                case "l": 
                    numdesc += "A large number of (over 10)"
                    mxtk += 250
                case _: numdesc += "Not sure how many"
            numdesc += " objects in total is expected to be cropped."
            prompt = "The task is to generate crops of the given image. Please find the following object(s) from the image: "
            prompt += desc+numdesc+" Answer how to crop by giving the percentage ranges on width and height to keep the original image, format is width a% to b%, height c% to d%. Do this for each object to crop."
            print(prompt)
            instr = mo.answer(prompt=prompt, image_url="static/imgorig/"+imgcrop, mtoken=mxtk)
            res = imf.crop_multiple(imgcrop, instr)
            imgcrop = "static/imgorig/"+imgcrop

    imggroups = imf.imggroups_all()
    return render_template('index.html', imggroups=imggroups, croporig=imgcrop, result=res, cropexpl=instr)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)