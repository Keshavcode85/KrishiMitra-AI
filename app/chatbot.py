import numpy as np
from PIL import Image

model = None

def load_model():
    global model
    if model is None:
        import tensorflow as tf
        model = tf.keras.models.load_model("model/plant_disease_model.h5")
    return model


def predict_disease(image_path):
    model = load_model()

    img = Image.open(image_path).resize((224,224))
    img = np.array(img)/255.0
    img = np.expand_dims(img,axis=0)

    prediction = model.predict(img)

    return prediction


def chatbot_response(message):
    message = message.lower()

    if "hello" in message:
        return "Hello 👋 I am KrishiMitra AI"

    if "disease" in message:
        return "Upload leaf image to detect disease 🌿"

    return "Sorry, I did not understand."