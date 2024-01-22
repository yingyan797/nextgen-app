# Y-Detective Image & Language AI Assistance Program
-- Utilize AI to expand human limits.

Combining computer vision and natural language processing, the program provides the following functionalities:
1. Multiple object detection from an image and auto cropping
2. Image searching and selection based on descriptions in natural language
3. Image grneration
4. Ask questions about an image
5. Text to speech generation

For object cropping, please select the image from "static/imgorig/" directory; for image selection, select from "static/imggroups/{class name}/" directory. For both, the result will be saved to "static/result/".

GPT-4 Vision, DALL E image generation, and OpenAI text to speech are used.
To use our AI tools, please obtain a Clarifai access key, create a .env file in the root directory, and put the key in the .env file as follows:

CLARIFAI_PAT="Your access key"

To launch our program, open "main.py" and click run. The webpage will be in local host.