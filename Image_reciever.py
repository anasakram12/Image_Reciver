from flask import Flask, request
import os
from datetime import datetime   


app = Flask(__name__)

# Directory to save the images
save_dir = "Received_Images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

@app.route('/save_image', methods=['POST'])
def save_image():
    if 'file1' not in request.files or 'file2' not in request.files:
        return "Missing files", 400

    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == '' or file2.filename == '':
        return "No selected file", 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    image_path1 = os.path.join(save_dir, f'captured_4k_image1_{timestamp}.jpg')
    image_path2 = os.path.join(save_dir, f'captured_4k_image2_{timestamp}.jpg')

    file1.save(image_path1)
    file2.save(image_path2)

    return "Images saved successfully"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
