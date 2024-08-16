from flask import Flask, render_template, request, redirect, url_for
import os
import base64
import re

app = Flask(__name__)

# Folder to store the uploaded images
UPLOAD_FOLDER = 'static/images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    data = request.get_json()
    image_data = data['image']

    # Decode the image data and save it
    image_data = re.sub('^data:image/.+;base64,', '', image_data)
    image_path = os.path.join(UPLOAD_FOLDER, 'captured_image.png')
    with open(image_path, "wb") as fh:
        fh.write(base64.b64decode(image_data))
    
    return 'Photo saved successfully!', 200

if __name__ == "__main__":
    app.run(debug=True)
