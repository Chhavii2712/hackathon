from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Load pre-trained models (replace with actual model paths)
plant_model = tf.keras.models.load_model('./plant_model.h5')  # Replace with your model path
disease_model = tf.keras.models.load_model('./disease_model.h5')  # Replace with your model path

# Preprocess image function
def preprocess_image(image):
    image = image.resize((224, 224))  # Resize to fit the model input
    image = np.array(image) / 255.0  # Normalize the image
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

# Plant Identification Function
def identify_plant(image):
    processed_image = preprocess_image(image)
    predictions = plant_model.predict(processed_image)
    predicted_class = np.argmax(predictions, axis=1)
    plant_species = ["Plant_A", "Plant_B", "Plant_C"]  # Replace with actual plant names
    return plant_species[predicted_class[0]]

# Disease Detection Function
def detect_disease(image):
    processed_image = preprocess_image(image)
    predictions = disease_model.predict(processed_image)
    predicted_class = np.argmax(predictions, axis=1)
    disease_classes = ["Healthy", "Leaf Spot", "Powdery Mildew", "Rust"]  # Example disease types
    return disease_classes[predicted_class[0]]

# Route for uploading an image and getting plant info
@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['file']
    image = Image.open(file.stream)

    # Identify plant
    plant_name = identify_plant(image)

    # Detect disease
    disease = detect_disease(image)

    # Return the results
    return jsonify({
        "plant_name": plant_name,
        "disease": disease
    })

if __name__ == '__main__':
    app.run(debug=True)
