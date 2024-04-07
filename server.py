from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from ultralytics import YOLO
import cv2
# import cvzone
import math
import time
import os
import torch
import base64
from PIL import Image
import io
import base64
from inference_sdk import InferenceHTTPClient
import requests
import tempfile

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

model = YOLO("yolov8n-pose.pt")

CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="HeBD4WDnlMGw1gNYeyM3"
    )

# def list_image_paths(folder_path):
#     image_paths = []
#     for root, dirs, files in os.walk(folder_path):
#         for file in files:
#             if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
#                 image_path = os.path.join(root, file)
#                 image_paths.append(image_path)
#     return image_paths

def list_image_paths(partial_folder_path):
    # Traverse the directory tree
    for root, dirs, files in os.walk("."):
        # Check if partial_folder_path is in the current root
        if partial_folder_path in root:
            # Print the first folder containing the partial folder path
            # print("First folder containing partial folder path:", root)
            # Now you can perform operations on the folder as needed
            # For example, you can enter the folder by changing the current working directory
            os.chdir(root)
            break

    # After entering the first folder containing the partial folder path
    # You can list the image paths within that folder
    image_paths = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_path = os.path.join(root, file)
                image_paths.append(image_path)
    return image_paths

# Define your routes
@app.route('/detect', methods=['POST'])
def api():
    # Access the data sent in the request
    data = request.json

    img = data['img']

    # Decode the Base64 string back into bytes
    image_data = base64.b64decode(img)

    # Open image from bytes
    image = Image.open(io.BytesIO(image_data))

    dir = 'adho makara mukha svanasana'
    # infer on a local image
    result = CLIENT.infer(image, model_id="yogaclassification/2")
    if len(result['predicted_classes']):
        dir = result['predicted_classes'][0]

    results1 = model(image)
    keypoints1 = results1[0].keypoints.xy[0]



    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_image:
        image.save(temp_image)

    # Read the temporary image using OpenCV
    img1 = cv2.imread(temp_image.name)
    for kpt in keypoints1:
    # print(kpt)
      x, y = int(kpt[0]), int(kpt[1])
      cv2.circle(img1, (x, y), radius=3, color=(0, 255, 0), thickness = 2)
    _, img1_encoded = cv2.imencode('.jpg', img1)

        # Encode the image data to Base64
    base64_img1 = base64.b64encode(img1_encoded).decode('utf-8')

    # # Use cv2.imdecode() to decode the image data
    # img1 = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    

    folder_path = 'Capstone-Project-1\\valid\\' + dir
    image_paths = list_image_paths(folder_path)
    print(len(image_paths))
    print('Capstone-Project-1\\valid\\' + dir)
    maxSim = 0
    #imgPath = 'F:\\yoga\\Capstone-Project-1\\valid\\adho makara mukha svanasana\\2-0_png.rf.0d9b80e738a35c9a31e0329a071febb5.jpg'

    for image_path in image_paths:
        results2 = model(image_path)
        keypoints2 = results2[0].keypoints.xy[0]
        try:
            # print(keypoints1)
            flat_tensor1 = keypoints1.flatten()
            flat_tensor2 = keypoints2.flatten()

            dot_product = torch.dot(flat_tensor1, flat_tensor2)
            norm1 = torch.norm(flat_tensor1)
            norm2 = torch.norm(flat_tensor2)
            cosine_similarity = dot_product / (norm1 * norm2)
            # print(cosine_similarity)

            if cosine_similarity.item() > maxSim:
                # print(imgPath)
                maxSim = cosine_similarity.item()
                imgPath = image_path

        except:
            print('0')

    try:
        img_data = cv2.imread(imgPath)
        for kpt in keypoints2:
        # print(kpt)
            x, y = int(kpt[0]), int(kpt[1])
            cv2.circle(img_data, (x, y), radius=3, color=(0, 255, 0), thickness = 2)
    # Encode the image data to Base64
    # Convert the modified image to JPEG format
        _, img_encoded = cv2.imencode('.jpg', img_data)

        # Encode the image data to Base64
        base64_encoded = base64.b64encode(img_encoded).decode('utf-8')
        # base64_encoded = base64.b64encode(img_data).decode('utf-8')
    # Process the data (replace this with your actual processing logic)
        result = base64_encoded
    except:
        return jsonify({'status':'unable to detect'})

    # print(dir)

    # Return a JSON response
    return jsonify({'img': result, 'inputImg': base64_img1 , 'prediction': dir, 'status':'able to detect'})

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
