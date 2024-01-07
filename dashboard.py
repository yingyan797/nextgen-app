from dotenv import load_dotenv
import os
from clarifai.client.model import Model

load_dotenv()
clarifai_pat = os.environ["CLARIFAI_PAT"]

prompt = "Mongolian dance"
inference_params = dict(quality="standard", size= '1024x1024')
model_prediction = Model("https://clarifai.com/openai/dall-e/models/dall-e-3").predict_by_bytes(prompt.encode(), input_type="text", inference_params=inference_params)
output_base64 = model_prediction.outputs[0].data.image.base64

f = open("result.png", "wb")
f.write(output_base64)
f.close()