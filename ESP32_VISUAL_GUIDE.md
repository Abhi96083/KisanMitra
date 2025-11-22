# ESP32 Integration - Visual Guide

## 🎯 Complete Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                   KishanMitra Web Application                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  User Browser (http://localhost:5000)                               │
│  ├─ Clicks "Crop" link in navbar                                    │
│  └─ Opens /crop-recommend route                                     │
│                    ↓                                                  │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │ crop.html loads                                            │     │
│  │ ├─ Shows page title & subtitle                            │     │
│  │ └─ JavaScript runs on page load:                          │     │
│  │    "document.addEventListener('DOMContentLoaded', ...)"   │     │
│  └────────────────────────────────────────────────────────────┘     │
│                    ↓                                                  │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │ Step 1: Show Loading Animation                            │     │
│  │ ├─ Display: "📡 Fetching ESP32 Sensor Data..."           │     │
│  │ ├─ Show spinning loader                                   │     │
│  │ └─ Hide sensor data & error containers                    │     │
│  └────────────────────────────────────────────────────────────┘     │
│                    ↓ (JavaScript fetch)                              │
└─────────────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────────┐
│              ESP32 Hardware (172.20.220.21)                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ NPK Sensor   │  │ DHT Sensor   │  │ pH Sensor    │              │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤              │
│  │ • Nitrogen   │  │ • Temp       │  │ • pH         │              │
│  │ • Phosphorus │  │ • Humidity   │  │              │              │
│  │ • Potassium  │  │              │  │              │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
│         ↓                  ↓                  ↓                      │
│  ┌──────────────────────────────────────────────────────────┐       │
│  │ ESP32 Microcontroller (172.20.220.21)                  │       │
│  ├──────────────────────────────────────────────────────────┤       │
│  │ Aggregates all sensor readings                         │       │
│  │ Creates JSON response at /readings endpoint            │       │
│  └──────────────────────────────────────────────────────────┘       │
│         ↑ HTTP GET Request ↑                                        │
└─────────────────────────────────────────────────────────────────────┘
                    ↑
                    │ fetch('http://172.20.220.21/readings')
                    │
┌─────────────────────────────────────────────────────────────────────┐
│  Browser sends HTTP request to ESP32                                │
│  (JavaScript CORS request - must be same local network)             │
└─────────────────────────────────────────────────────────────────────┘
         ↓ HTTP Response (JSON)
┌─────────────────────────────────────────────────────────────────────┐
│  ESP32 Returns JSON:                                                 │
│  {                                                                   │
│    "nitrogen": 45,                                                  │
│    "phosphorus": 35,                                                │
│    "potassium": 40,                                                 │
│    "temperature_dht": 28.5,                                         │
│    "humidity": 75.2,                                                │
│    "ph": 7.1,                                                       │
│    "moisture": 55.8                                                 │
│  }                                                                   │
└─────────────────────────────────────────────────────────────────────┘
         ↓ JavaScript processes response
┌─────────────────────────────────────────────────────────────────────┐
│  JavaScript in crop.html:                                            │
│  ├─ Hide loading animation                                          │
│  ├─ Display sensor values:                                          │
│  │  • Nitrogen (N): 45 ppm                                          │
│  │  • Phosphorus (P): 35 ppm                                        │
│  │  • Potassium (K): 40 ppm                                         │
│  │  • Temperature: 28.50 °C                                         │
│  │  • Humidity: 75.20 %                                             │
│  │  • pH: 7.10                                                      │
│  │  • Moisture (Rainfall): 55.80 mm                                 │
│  │                                                                  │
│  ├─ Populate hidden form fields:                                   │
│  │  <input name="nitrogen" value="45" />                           │
│  │  <input name="phosphorous" value="35" />                        │
│  │  <input name="pottasium" value="40" />                          │
│  │  ... (all 7 fields)                                             │
│  │                                                                  │
│  └─ Auto-submit form to /crop-predict after 2 seconds              │
└─────────────────────────────────────────────────────────────────────┘
         ↓ Form POST request with sensor data
┌─────────────────────────────────────────────────────────────────────┐
│  Flask Backend (app.py)                                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  /crop-predict route receives form data                             │
│  {                                                                   │
│    nitrogen: "45",                                                  │
│    phosphorous: "35",                                               │
│    pottasium: "40",                                                 │
│    ph: "7.1",                                                       │
│    rainfall: "55.8"                                                 │
│  }                                                                   │
│                    ↓                                                  │
│  ┌─────────────────────────────────────────────────────────┐        │
│  │ Step 1: Extract sensor data from form                   │        │
│  │ N = 45, P = 35, K = 40                                 │        │
│  │ temperature = 28.5°C, humidity = 75.2%                 │        │
│  │ ph = 7.1, rainfall = 55.8mm                            │        │
│  └─────────────────────────────────────────────────────────┘        │
│                    ↓                                                  │
│  ┌─────────────────────────────────────────────────────────┐        │
│  │ Step 2: Prepare data array for model                    │        │
│  │ data = np.array([[45, 35, 40, 28.5, 75.2, 7.1, 55.8]])│        │
│  └─────────────────────────────────────────────────────────┘        │
│                    ↓                                                  │
│  ┌─────────────────────────────────────────────────────────┐        │
│  │ Step 3: Call ML Model (UNCHANGED)                       │        │
│  │ ┌────────────────────────────────────────────────────┐ │        │
│  │ │ RandomForest Classifier                            │ │        │
│  │ │ (models/RandomForest.pkl)                          │ │        │
│  │ │                                                    │ │        │
│  │ │ my_prediction = model.predict(data)              │ │        │
│  │ │ # Returns: ['Rice']                              │ │        │
│  │ └────────────────────────────────────────────────────┘ │        │
│  └─────────────────────────────────────────────────────────┘        │
│                    ↓                                                  │
│  ┌─────────────────────────────────────────────────────────┐        │
│  │ Step 4: Prepare response data                           │        │
│  │ sensor_data = {                                        │        │
│  │   'N': 45, 'P': 35, 'K': 40,                          │        │
│  │   'temperature': 28.5, 'humidity': 75.2,             │        │
│  │   'ph': 7.1, 'rainfall': 55.8,                       │        │
│  │   'source': 'ESP32'                                  │        │
│  │ }                                                     │        │
│  │                                                      │        │
│  │ return render_template('crop-result.html',          │        │
│  │   prediction='Rice',                                │        │
│  │   sensor_data=sensor_data                           │        │
│  │ )                                                    │        │
│  └─────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────┘
         ↓ HTML response
┌─────────────────────────────────────────────────────────────────────┐
│  Browser displays crop-result.html                                  │
│                                                                      │
│  ┌────────────────────────────────────────┐                        │
│  │ Recommended Crop: 🌾 RICE              │                        │
│  └────────────────────────────────────────┘                        │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │ 📡 ESP32 Sensor Data Used for Prediction:              │       │
│  ├─────────────────────────────────────────────────────────┤       │
│  │ • Nitrogen (N):      45 ppm                            │       │
│  │ • Phosphorus (P):    35 ppm                            │       │
│  │ • Potassium (K):     40 ppm                            │       │
│  │ • Temperature:       28.50 °C                          │       │
│  │ • Humidity:          75.20 %                           │       │
│  │ • pH Level:          7.10                              │       │
│  │ • Moisture (Rain):   55.80 mm                          │       │
│  │ • Data Source:       ESP32                             │       │
│  └─────────────────────────────────────────────────────────┘       │
│                                                                      │
│  [← Back to Home]                                                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Error Handling Flow

```
┌──────────────────────────────┐
│ ESP32 Fetch Starts           │
└────────────┬─────────────────┘
             │
        ┌────▼─────┐
        │ Is ESP32  │
        │ Online?   │
        └────┬──────┘
             │
     ┌───────┴────────┐
     │                │
  YES│              NO│
     │                │
     ▼                ▼
┌─────────────┐  ┌──────────────────────────┐
│ Display     │  │ Show Error Message:      │
│ Sensor Data │  │ ❌ "Sensor Connection   │
│             │  │ Error"                   │
│ Auto-Submit │  │                          │
│ Form        │  │ [Retry Button]           │
└─────────────┘  └──────────────────────────┘
     │                      │
     │                   User clicks
     │                   Retry
     │                      │
     ▼                      │
  SUCCESS              ┌────▴─────┐
  Crop Result          │ Try Again │
  Displayed            │ (loop back)
                       └──────────┘
```

---

## 🎨 UI State Transitions

```
┌─────────────────────────────────────────────────┐
│                 crop.html States                 │
├─────────────────────────────────────────────────┤

Initial State:
┌───────────────────────────────────────────────┐
│ Loading Container: HIDDEN                     │
│ Sensor Data Container: HIDDEN                 │
│ Error Container: HIDDEN                       │
│ Hidden Form: exists but not visible           │
└───────────────────────────────────────────────┘
        ↓
Page Load Event Triggers fetchAndPredictCrop()
        ↓
┌───────────────────────────────────────────────┐
│ Loading State:                                │
│ ┌─────────────────────────────────────────┐  │
│ │ 📡 Fetching ESP32 Sensor Data...        │  │
│ │ [spinner animation]                     │  │
│ │ Please wait...                          │  │
│ └─────────────────────────────────────────┘  │
│ Loading Container: VISIBLE                    │
│ Sensor Data Container: HIDDEN                 │
│ Error Container: HIDDEN                       │
└───────────────────────────────────────────────┘
        ↓ (ESP32 responds)
┌───────────────────────────────────────────────┐
│ Data Received State:                          │
│ ┌─────────────────────────────────────────┐  │
│ │ ✅ ESP32 Sensor Data Received:          │  │
│ │                                         │  │
│ │ Nitrogen (N):      45 ppm               │  │
│ │ Phosphorus (P):    35 ppm               │  │
│ │ Potassium (K):     40 ppm               │  │
│ │ Temperature:       28.50 °C             │  │
│ │ Humidity:          75.20 %              │  │
│ │ pH:                7.10                 │  │
│ │ Moisture (Rainfall):55.80 mm            │  │
│ │                                         │  │
│ │ Processing with RandomForest model...   │  │
│ └─────────────────────────────────────────┘  │
│ Loading Container: HIDDEN                     │
│ Sensor Data Container: VISIBLE                │
│ Error Container: HIDDEN                       │
└───────────────────────────────────────────────┘
        ↓ (2 seconds)
       Auto-Submit Form
        ↓
  Flask processes
        ↓
   Redirect to Results
        ↓
┌───────────────────────────────────────────────┐
│ crop-result.html displays:                   │
│ • Recommended Crop: RICE                      │
│ • All Sensor Data Table                       │
│ • Back Button                                 │
└───────────────────────────────────────────────┘

Alternative: If ESP32 Offline
        ↓
┌───────────────────────────────────────────────┐
│ Error State:                                 │
│ ┌─────────────────────────────────────────┐  │
│ │ ❌ Sensor Connection Error               │  │
│ │                                         │  │
│ │ Unable to connect to ESP32 sensor.     │  │
│ │ Please check the device connection     │  │
│ │ and try again.                         │  │
│ │                                         │  │
│ │ [Retry]                                 │  │
│ └─────────────────────────────────────────┘  │
│ Loading Container: HIDDEN                     │
│ Sensor Data Container: HIDDEN                 │
│ Error Container: VISIBLE                      │
└───────────────────────────────────────────────┘
        ↓ (User clicks Retry)
   Start Over (loop back to Loading State)
```

---

## 📡 Network Communication

```
┌─────────────────────────────────────────────────────┐
│ LOCAL NETWORK (192.168.x.x range or similar)        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────┐        ┌──────────────────┐  │
│  │  Your Computer   │        │  ESP32 Device    │  │
│  │  (runs Flask app)│        │ (IP: 172.20...)  │  │
│  │                  │        │                  │  │
│  │  localhost:5000  │◄──────►│  :80/readings    │  │
│  │  (Flask server)  │ HTTP   │ (JSON endpoint)  │  │
│  │                  │ GET    │                  │  │
│  │  Browser:        │        │  Sensors:        │  │
│  │  ├─ crop.html    │        │  ├─ NPK          │  │
│  │  ├─ JavaScript   │        │  ├─ DHT (T+H)    │  │
│  │  └─ fetch()      │        │  ├─ pH           │  │
│  │                  │        │  └─ Moisture     │  │
│  └──────────────────┘        └──────────────────┘  │
│                                                     │
│  Must be on same network!                           │
│  (Both need Wi-Fi access or connected via Ethernet)│
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🔌 Hardware Connections

```
ESP32 Microcontroller (172.20.220.21)

┌─────────────────────────────────────────┐
│           ESP32 Pinout                   │
├─────────────────────────────────────────┤
│                                          │
│  GPIO Pins Connected to:                │
│                                          │
│  A0/ADC1  ──► NPK Sensor                │
│             (Analog output)             │
│             ├─ Nitrogen pin             │
│             ├─ Phosphorus pin           │
│             └─ Potassium pin            │
│                                          │
│  GPIO 4,5 ──► DHT22 Sensor              │
│             (Digital output)            │
│             ├─ Temperature              │
│             └─ Humidity                 │
│                                          │
│  A3/ADC3  ──► pH Sensor                 │
│             (Analog output)             │
│             └─ pH probe                 │
│                                          │
│  GPIO 32  ──► Moisture Sensor           │
│             (Analog output)             │
│             └─ Capacitive sensor        │
│                                          │
│  GPIO 1,3 ──► WiFi Module               │
│             (Built-in ESP32 WiFi)      │
│             ├─ Connects to router       │
│             └─ Hosts /readings endpoint │
│                                          │
│  GND ─────────► Common Ground           │
│  3.3V/5V ─────► Power supply            │
│                                          │
└─────────────────────────────────────────┘
```

---

## 🔐 Data Security Flow

```
┌─────────────────────────────────────────────────┐
│ Local Network Only (Secure)                     │
├─────────────────────────────────────────────────┤
│                                                 │
│ ✅ No External Internet                         │
│ ✅ No Cloud Upload                              │
│ ✅ No Data Collection                           │
│ ✅ No Authentication Required (private network) │
│ ✅ Real-time Processing                         │
│ ✅ Farmer's Data Stays Local                    │
│                                                 │
│ If Deployed on Internet:                        │
│ ⚠️  Should add HTTPS                            │
│ ⚠️  Should add API key/token                    │
│ ⚠️  Should rate-limit requests                  │
│ ⚠️  Should use VPN if public                    │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

**This visual guide shows the complete journey from clicking "Crop" to seeing the recommended crop with sensor data.**
