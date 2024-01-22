from dotenv import load_dotenv
import os
from clarifai.client.model import Model
import base64

load_dotenv()
clarifai_pat = os.environ["CLARIFAI_PAT"]

def image_gen(prompt="Mongolian dance", infparams=dict(quality="standard", size= '1024x1024'), fn=""):
    if not fn:
        fn = "imggen"
    dest = "static/result/"+fn+".png"
    model_prediction = Model("https://clarifai.com/openai/dall-e/models/dall-e-3").predict_by_bytes(prompt.encode(), input_type="text", inference_params=infparams)
    output_base64 = model_prediction.outputs[0].data.image.base64
    f = open(dest, "wb")
    f.write(output_base64)
    f.close()

def answer(prompt, image_url="", mtoken = 250, infparams=dict(temperature=0.2), dest=""):
    infparams["max_tokens"] = mtoken
    modelname = "turbo"
    if image_url:
        modelname = "vision"
        f = open(image_url, "rb")
        b64img = base64.b64encode(f.read()).decode('utf-8')
        f.close()
        infparams["image_base64"] = b64img
    model_prediction = Model("https://clarifai.com/openai/chat-completion/models/gpt-4-"+modelname).predict_by_bytes(prompt.encode(), input_type="text", inference_params=infparams)
    ans = model_prediction.outputs[0].data.text.raw
    if dest:
        f = open("static/"+dest+".txt", "a")
        f.write("--Q: "+prompt+"-- "+image_url+'\n'+ans+"\n\n")
        f.close()
    return ans

def text_speech(text, infparams=dict(voice="alloy", speed=1.0), fn=""):
    if not fn:
        fn = "speech"
    dest = "static/result/"+fn+".mp3"
    model_prediction = Model("https://clarifai.com/openai/tts/models/openai-tts-1").predict_by_bytes(text.encode(), input_type="text", inference_params=infparams)
    output_base64 = model_prediction.outputs[0].data.audio.base64
    f = open(dest, "wb")
    f.write(output_base64)
    f.close()
