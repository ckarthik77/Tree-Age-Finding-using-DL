from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Load pre-trained model (Replace 'model.h5' with your trained model file)
model = tf.keras.models.load_model('tree_age_model.h5')

def preprocess_image(image):
    image = image.resize((128, 128))  # Resize to model input shape
    image = np.array(image) / 255.0   # Normalize
    image = np.expand_dims(image, axis=0)  # Expand dimensions for model input
    return image

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    image = Image.open(io.BytesIO(file.read()))
    processed_image = preprocess_image(image)
    
    prediction = model.predict(processed_image)
    estimated_age = int(prediction[0][0])  # Assuming regression model output
    
    return jsonify({'estimated_age': estimated_age})

if __name__ == '__main__':
    app.run(debug=True)
