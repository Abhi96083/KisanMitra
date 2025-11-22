# Importing essential libraries and modules

from flask import Flask, render_template, request, Markup, session
import numpy as np
import pandas as pd
from utils.disease import disease_dic
from utils.disease_translator import get_disease_description
from utils.fertilizer import fertilizer_dic
from utils.fertilizer_translator import get_fertilizer_recommendation
import requests
import config
import pickle
import io
import torch
from torchvision import transforms
import cv2
from PIL import Image
from utils.model import ResNet9
import json
import os

# ============================================
# ESP32 SENSOR URL (UPDATED)
ESP_URL = "http://10.126.227.21/readings"
# ============================================

# ------------------------- LOADING MODELS -----------------------------------

disease_classes = [
 'Apple___Apple_scab','Apple___Black_rot','Apple___Cedar_apple_rust',
 'Apple___healthy','Blueberry___healthy','Cherry_(including_sour)___Powdery_mildew',
 'Cherry_(including_sour)___healthy','Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
 'Corn_(maize)___Common_rust_','Corn_(maize)___Northern_Leaf_Blight','Corn_(maize)___healthy',
 'Grape___Black_rot','Grape___Esca_(Black_Measles)','Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
 'Grape___healthy','Orange___Haunglongbing_(Citrus_greening)','Peach___Bacterial_spot',
 'Peach___healthy','Pepper,_bell___Bacterial_spot','Pepper,_bell___healthy','Potato___Early_blight',
 'Potato___Late_blight','Potato___healthy','Raspberry___healthy','Soybean___healthy',
 'Squash___Powdery_mildew','Strawberry___Leaf_scorch','Strawberry___healthy','Tomato___Bacterial_spot',
 'Tomato___Early_blight','Tomato___Late_blight','Tomato___Leaf_Mold','Tomato___Septoria_leaf_spot',
 'Tomato___Spider_mites Two-spotted_spider_mite','Tomato___Target_Spot',
 'Tomato___Tomato_Yellow_Leaf_Curl_Virus','Tomato___Tomato_mosaic_virus','Tomato___healthy'
]

disease_model_path = 'models/plant_disease_model.pth'
disease_model = ResNet9(3, len(disease_classes))
disease_model.load_state_dict(torch.load(disease_model_path, map_location=torch.device('cpu')))
disease_model.eval()

crop_recommendation_model_path = 'models/RandomForest.pkl'
crop_recommendation_model = pickle.load(open(crop_recommendation_model_path, 'rb'))

# ============================================
# SENSOR FETCH FUNCTION
def fetch_esp_data():
    try:
        r = requests.get(ESP_URL, timeout=4)
        data = r.json()
        return data
    except:
        return None
# ============================================


def is_leaf_image(img_bytes):
    file_bytes = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([25, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    return cv2.countNonZero(mask) >= 1800


def predict_image(img, model=disease_model):
    transform = transforms.Compose([transforms.Resize(256), transforms.ToTensor()])
    image = Image.open(io.BytesIO(img))
    img_t = transform(image)
    img_u = torch.unsqueeze(img_t, 0)
    yb = model(img_u)
    probs = torch.nn.functional.softmax(yb, dim=1)
    max_prob, preds = torch.max(probs, dim=1)
    if max_prob.item() < 0.6:
        return "Unknown or Not a Leaf"
    return disease_classes[preds[0].item()]


app = Flask(__name__)

# Configure session
app.secret_key = 'your-secret-key-change-in-production'
app.config['SESSION_TYPE'] = 'filesystem'

# Load translations
def load_translations(lang_code):
    """Load translation dictionary for given language code"""
    translations_path = os.path.join(os.path.dirname(__file__), 'static', 'translations', f'{lang_code}.json')
    try:
        with open(translations_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to English if language file not found
        with open(os.path.join(os.path.dirname(__file__), 'static', 'translations', 'en.json'), 'r', encoding='utf-8') as f:
            return json.load(f)

# Context processor to inject translations into all templates
@app.context_processor
def inject_translations():
    """Inject translations into template context"""
    lang = session.get('language', 'en')
    translations = load_translations(lang)
    return dict(translations=translations, current_lang=lang)

# Language switching route
@app.route('/set-language/<lang>')
def set_language(lang):
    """Set the user's preferred language"""
    if lang in ['en', 'hi', 'kn']:
        session['language'] = lang
    return 'Language set successfully', 200

# ===============================================================================
# 🔌 ESP32 SENSOR PROXY (Solves CORS Issues)
@app.route('/api/sensor-data', methods=['GET'])
def sensor_proxy():
    """
    Proxy endpoint for ESP32 sensor data.
    Solves CORS issues by routing through Flask server instead of direct browser request.
    Browser -> Flask (localhost) -> ESP32 (10.126.227.21)
    """
    try:
        sensor_data = fetch_esp_data()
        if sensor_data is None:
            return {'error': 'Could not fetch ESP32 data', 'status': 'offline'}, 503
        return sensor_data, 200
    except Exception as e:
        return {'error': str(e), 'status': 'error'}, 500

# ===============================================================================

@app.route('/')
def home():
    return render_template('index.html', title='Harvestify - Home')


@app.route('/crop-recommend')
def crop_recommend():
    return render_template('crop.html', title='Harvestify - Crop Recommendation')


# 🌱 AUTO SENSOR CROP PREDICTION (ESP32 JSON INPUT)
@app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    """
    Crop prediction route that accepts:
    1. Automatic ESP32 data (if no form fields provided)
    2. Form data with manual inputs (N, P, K, temperature, humidity, ph, rainfall)
    
    ML Model (crop_recommendation_model.predict) remains completely unchanged.
    """
    
    # Check if form has explicit field values (manual submission)
    if request.form.get('nitrogen') and request.form.get('phosphorous'):
        # Use form data if provided
        N = float(request.form.get('nitrogen', 20))
        P = float(request.form.get('phosphorous', 10))
        K = float(request.form.get('pottasium', 30))
        temperature = float(request.form.get('temperature', 25)) if request.form.get('temperature') else None
        humidity = float(request.form.get('humidity', 60)) if request.form.get('humidity') else None
        ph = float(request.form.get('ph', 6.5))
        rainfall = float(request.form.get('rainfall', 50))
        
        # If temperature/humidity missing from form, fetch from ESP32 as fallback
        if temperature is None or humidity is None:
            sensor = fetch_esp_data()
            if sensor:
                if temperature is None:
                    temperature = float(sensor.get("temperature_dht", 25))
                if humidity is None:
                    humidity = float(sensor.get("humidity", 60))
    else:
        # Auto fetch from ESP32 if no form data
        sensor = fetch_esp_data()
        
        if sensor is None:
            return render_template('try_again.html', title="Sensor Error")
        
        # Fetch all values from ESP32
        N = float(sensor.get("nitrogen", 20))
        P = float(sensor.get("phosphorus", 10))
        K = float(sensor.get("potassium", 30))
        temperature = float(sensor.get("temperature", 25))
        humidity = float(sensor.get("humidity", 60))
        ph = float(sensor.get("ph", 6.5))
        rainfall = float(sensor.get("rainfall", 50))

    # Prepare data for model (unchanged ML code)
    data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    
    # ML Model prediction - COMPLETELY UNCHANGED
    my_prediction = crop_recommendation_model.predict(data)
    final_prediction = my_prediction[0]

    # Pass sensor data to template for display
    sensor_data = {
        'N': N,
        'P': P,
        'K': K,
        'temperature': temperature,
        'humidity': humidity,
        'ph': ph,
        'rainfall': rainfall,
        'source': 'ESP32'
    }

    return render_template(
        'crop-result.html',
        prediction=final_prediction,
        sensor_data=sensor_data,
        title='Harvestify - Crop Recommendation'
    )


@app.route('/fertilizer')
def fertilizer_recommendation():
    return render_template('fertilizer.html', title="Harvestify - Fertilizer Suggestion")


@app.route('/fertilizer-predict', methods=['POST'])
def fert_recommend():
    crop_name = str(request.form['cropname'])
    N = int(request.form['nitrogen'])
    P = int(request.form['phosphorous'])
    K = int(request.form['pottasium'])

    df = pd.read_csv('Data/fertilizer.csv')
    nr = df[df['Crop'] == crop_name]['N'].iloc[0]
    pr = df[df['Crop'] == crop_name]['P'].iloc[0]
    kr = df[df['Crop'] == crop_name]['K'].iloc[0]

    n = nr - N
    p = pr - P
    k = kr - K
    temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
    max_value = temp[max(temp.keys())]

    if max_value == "N":
        key = "NHigh" if n < 0 else "Nlow"
    elif max_value == "P":
        key = "PHigh" if p < 0 else "Plow"
    else:
        key = "KHigh" if k < 0 else "Klow"

    # Get language from session, default to English
    lang = session.get('language', 'en')
    
    # Get multilingual recommendation
    response = Markup(get_fertilizer_recommendation(key, lang))
    
    return render_template('fertilizer-result.html', recommendation=response)


@app.route('/disease-predict', methods=['GET', 'POST'])
def disease_prediction():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            return render_template('disease.html')

        img = file.read()
        if not is_leaf_image(img):
            # Get multilingual message for no leaf detected
            lang = session.get('language', 'en')
            if lang == 'hi':
                message = "⚠️ कोई वैध पत्ती पाई नहीं गई! कृपया एक स्पष्ट पत्ती की तस्वीर अपलोड करें।"
            elif lang == 'kn':
                message = "⚠️ ಯಾವುದೇ ವೈಧ ಪತ್ರೆ ಕಂಡುಹಿಡಿಯಲಾಗಿಲ್ಲ! ದಯವಿಟ್ಟು ಸ್ಪಷ್ಟ ಪತ್ರೆ ಛಾಯಾ ಅಪ್ಲೋಡ್ ಮಾಡಿ।"
            else:
                message = "⚠️ No valid leaf detected! Please upload a leaf photo."
            
            return render_template('disease-result.html', prediction=message)

        # Get ML prediction (unchanged)
        disease_name = predict_image(img)

        # Get multilingual description using the translator
        lang = session.get('language', 'en')
        prediction_text = get_disease_description(disease_name, lang)
        
        # Fallback to English if translation not found
        if not prediction_text:
            prediction_text = get_disease_description(disease_name, 'en')
        
        prediction = Markup(prediction_text)

        return render_template('disease-result.html', prediction=prediction)

    return render_template('disease.html')


# ================================================================
if __name__ == '__main__':
    app.run(debug=False)
