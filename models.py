from dotenv import load_dotenv
import os
from clarifai.client.model import Model

load_dotenv()
clarifai_pat = os.environ["CLARIFAI_PAT"]

def image_gen(prompt="Mongolian dance", infparams=dict(quality="standard", size= '1024x1024')):
    model_prediction = Model("https://clarifai.com/openai/dall-e/models/dall-e-3").predict_by_bytes(prompt.encode(), input_type="text", inference_params=infparams)
    output_base64 = model_prediction.outputs[0].data.image.base64
    f = open("static/res_image.png", "wb")
    f.write(output_base64)
    f.close()

def answer(prompt, image_url="", infparams=dict(temperature=0.2, max_tokens=100)):
    if image_url:
        print("Asking about image:",image_url)
        infparams["image_url"] = image_url
    model_prediction = Model("https://clarifai.com/openai/chat-completion/models/gpt-4-vision").predict_by_bytes(prompt.encode(), input_type="text", inference_params=infparams)
    return model_prediction.outputs[0].data.text.raw

def text_speech(text, infparams=dict(voice="alloy", speed=1.0)):
    model_prediction = Model("https://clarifai.com/openai/tts/models/openai-tts-1").predict_by_bytes(text.encode(), input_type="text", inference_params=infparams)
    output_base64 = model_prediction.outputs[0].data.audio.base64
    f = open("static/res_audio.mp3", "wb")
    f.write(output_base64)
    f.close()
