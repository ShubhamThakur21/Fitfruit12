from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploaded'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the model
model = load_model('mango_ripeness_classifier.h5')

# Preprocess image
def preprocess_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (64, 64))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Classify image
def classify_image(img_path):
    img = preprocess_image(img_path)
    prediction = model.predict(img)[0][0]
    return "Artificially Ripened" if prediction < 0.5 else "Naturally Ripened"

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return redirect(url_for('index'))

    file = request.files['image']
    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Classify the uploaded image
        result = classify_image(filepath)
        return render_template('result.html', image_url=filepath, result=result)

if __name__ == '__main__':
    app.run(debug=True)
