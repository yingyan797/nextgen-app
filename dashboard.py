from flask import Flask, render_template, request
import imagegen

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])    # main page
def index():
    prompt = request.form.get('prompt')
    if prompt:
        imagegen.generate(prompt=prompt)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)