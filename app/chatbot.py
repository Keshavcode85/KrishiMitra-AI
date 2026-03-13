import tensorflow as tf
import numpy as np
from PIL import Image
import requests
import os

# -------------------------------
# LOAD AI MODEL (Render Safe Path)
# -------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "plant_disease_model.h5")

model = tf.keras.models.load_model(MODEL_PATH)

# -------------------------------
# CLASS LABELS
# -------------------------------

classes = [
    "Potato Early Blight",
    "Potato Late Blight",
    "Maize Rust",
    "Rice Leaf Blast",
    "Wheat Leaf Rust",
    "Healthy"
]

# -------------------------------
# MEDICINE DATABASE
# -------------------------------

medicine = {
    "Potato Early Blight": "Mancozeb Fungicide Spray",
    "Potato Late Blight": "Metalaxyl Spray",
    "Maize Rust": "Propiconazole Spray",
    "Rice Leaf Blast": "Tricyclazole Spray",
    "Wheat Leaf Rust": "Tilt Fungicide",
    "Healthy": "No disease detected"
}

# -------------------------------
# WEATHER API
# -------------------------------

API_KEY = "42872c9adfa7373605ac509b9b3eb975"


def get_weather(city):

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)
        data = response.json()

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        return weather, temp, humidity

    except:
        return "Unknown", 0, 0


# -------------------------------
# CROP RECOMMENDATION
# -------------------------------

def recommend_crop(temp, humidity):

    if temp > 30 and humidity > 60:
        return "Rice 🌾"

    elif temp > 25 and humidity < 50:
        return "Wheat 🌾"

    elif temp > 28:
        return "Maize 🌽"

    else:
        return "Potato 🥔"


# -------------------------------
# DISEASE DETECTION
# -------------------------------

def predict_disease(image_path):

    img = Image.open(image_path).resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)

    index = np.argmax(prediction)

    disease = classes[index]

    return disease, medicine[disease]


# -------------------------------
# CHATBOT RESPONSE
# -------------------------------

def chatbot_response(message):

    message = message.lower()

    # WEATHER + CROP RECOMMENDATION
    if "recommend crop" in message:

        words = message.split()
        city = words[-1]

        weather, temp, humidity = get_weather(city)

        crop = recommend_crop(temp, humidity)

        return f"""
Weather in {city}

Condition: {weather}
Temperature: {temp}°C
Humidity: {humidity}%

Recommended Crop:
{crop}
"""

    elif "fertilizer" in message:
        return "Recommended fertilizer: NPK balanced fertilizer."

    elif "hello" in message:
        return "Hello Farmer 👋 How can I help you?"

    else:
        return "Ask me about crop recommendation, plant disease or fertilizer."
