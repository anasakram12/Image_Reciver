from flask import Flask, render_template_string, request
import cv2
import requests
import os
import time

app = Flask(__name__)

# Initialize the cameras with 4K resolution (adjust indices based on your cameras)
cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

# HTML template with a button to capture images from both cameras
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Capture Images</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(to right, #00c6ff, #0072ff);
            font-family: Arial, sans-serif;
            color: #fff;
            text-align: center;
        }
        .container {
            background: rgba(0, 0, 0, 0.5);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        }
        button {
            background-color: #0072ff;
            color: white;
            padding: 15px 25px;
            font-size: 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #005bb5;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Capture Images from Cameras</h1>
        <button onclick="captureImages()">Capture Images from Both Cameras</button>
    </div>
    <script>
        function captureImages() {
            fetch('/capture', { method: 'POST' })
            .then(response => response.text())
            .then(data => alert(data));
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/capture', methods=['POST'])
def capture_images():
    success1, frame1 = cap1.read()
    success2, frame2 = cap2.read()

    if success1 and success2:
        image_path1 = 'captured_image_camera1.jpg'
        image_path2 = 'captured_image_camera2.jpg'
        
        cv2.imwrite(image_path1, frame1)
        cv2.imwrite(image_path2, frame2)

        # Send the images to PC B
        pc_b_url = "http://192.168.1.169:5001/save_image"  # Replace with the actual IP of PC B
        with open(image_path1, 'rb') as f1, open(image_path2, 'rb') as f2:
            files = {'file1': f1, 'file2': f2}
            response = requests.post(pc_b_url, files=files)

            if response.status_code == 200:
                return "Images captured and saved successfully"
            else:
                return "Failed to save images to PC B", 500
    else:
        return "Failed to capture images", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
