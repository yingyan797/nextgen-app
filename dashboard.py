from flask import Flask, render_template, request
import models as mo

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
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)