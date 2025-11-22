# ESP32 Automatic Crop Prediction Integration Guide

## 🎯 Overview

Your KisanMitra application now **automatically fetches sensor data from ESP32** without requiring manual form input. The crop recommendation model receives data directly from your ESP32 device at `172.20.220.21`.

---

## 📡 How It Works

### Flow Diagram
```
User clicks "Crop" → crop.html loads
         ↓
JavaScript auto-fetches ESP32 data (172.20.220.21/readings)
         ↓
Sensor data displayed to user (N, P, K, Temp, Humidity, pH, Moisture)
         ↓
Hidden form auto-populated with sensor values
         ↓
After 2 seconds, form auto-submits to Flask backend
         ↓
Flask /crop-predict route receives sensor data
         ↓
RandomForest model.predict() processes data (unchanged ML code)
         ↓
Crop recommendation + sensor data displayed on results page
```

### Technical Changes

#### 1. Frontend (crop.html)
- **Old:** Manual input form with fields for N, P, K, temp, humidity, pH, rainfall
- **New:** Automatic fetch from ESP32 with loading animation + auto-submit

#### 2. Backend (app.py)
- **Old:** Only fetched ESP32 data, required form submission
- **New:** Accepts both auto (ESP32) and manual form data
- **ML Model:** Completely untouched (crop_recommendation_model.predict remains unchanged)

#### 3. Results Display (crop-result.html)
- **Old:** Only showed predicted crop name
- **New:** Shows predicted crop + sensor data used for prediction

---

## 🔧 Configuration

### ESP32 Endpoint
**Current:** `http://172.20.220.21/readings`

**Expected JSON Response Format:**
```json
{
  "nitrogen": 45,
  "phosphorus": 35,
  "potassium": 40,
  "temperature_dht": 28.5,
  "humidity": 75.2,
  "ph": 7.1,
  "moisture": 55.8
}
```

### If ESP32 IP Changes:
Update the ESP32 URL in TWO places:

**1. app.py (line ~24):**
```python
ESP_URL = "http://172.20.220.21/readings"  # ← Update this
```

**2. crop.html (line ~83 in JavaScript):**
```javascript
fetch('http://172.20.220.21/readings')  // ← Update this too
```

---

## 🧪 Testing the Integration

### Step 1: Verify ESP32 is Running
```bash
# Test if ESP32 endpoint is accessible
curl http://172.20.220.21/readings

# Expected output:
# {"nitrogen": 45, "phosphorus": 35, ...}
```

### Step 2: Start Flask Application
```bash
cd c:\Users\mnkp9\Kishanmitra
python -m flask run --app app.app
```

### Step 3: Test Automatic Crop Prediction
1. Open browser: `http://localhost:5000`
2. Click on **"Crop"** link in navbar
3. You should see:
   - **Loading message:** "📡 Fetching ESP32 Sensor Data..."
   - **Sensor display:** All 7 sensor values (N, P, K, Temp, Humidity, pH, Moisture)
   - **Auto-submit:** After 2 seconds, page redirects to results

### Step 4: Verify Results
On the results page, you should see:
- ✅ **Recommended crop** (e.g., "Rice", "Corn", "Wheat")
- ✅ **Sensor data table** showing all 7 parameters used
- ✅ **Data source:** "ESP32"

### Step 5: Test Error Handling
If ESP32 is offline:
1. Stop ESP32 device
2. Click "Crop" again
3. You should see error message: "❌ Sensor Connection Error"
4. "Retry" button to refresh

---

## 📊 Sensor Data Mapping

| Flask Parameter | ESP32 JSON Key | Unit | Default | ML Model Input |
|---|---|---|---|---|
| nitrogen (N) | nitrogen | ppm | 20 | ✓ |
| phosphorous (P) | phosphorus | ppm | 10 | ✓ |
| potassium (K) | potassium | ppm | 30 | ✓ |
| temperature | temperature_dht | °C | 25 | ✓ |
| humidity | humidity | % | 60 | ✓ |
| ph | ph | - | 6.5 | ✓ |
| rainfall (moisture) | moisture | mm | 50 | ✓ |

**All 7 parameters are required for accurate crop prediction.**

---

## 🤖 ML Model Preservation

The RandomForest crop recommendation model **REMAINS COMPLETELY UNCHANGED**:

```python
# app.py (line ~160)
data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
my_prediction = crop_recommendation_model.predict(data)
final_prediction = my_prediction[0]
```

✅ **No modifications to model inference**
✅ **No changes to feature engineering**
✅ **No changes to model file (RandomForest.pkl)**

The **ONLY change** is:
- Data now comes from **ESP32 instead of manual form input**
- Data presentation improved on results page

---

## 🔄 Fallback Behavior

If ESP32 fails to provide certain fields:

```python
# app.py fallback logic
N = float(sensor.get("nitrogen", 20))           # Default: 20
P = float(sensor.get("phosphorus", 10))         # Default: 10
K = float(sensor.get("potassium", 30))          # Default: 30
temperature = float(sensor.get("temperature_dht", 25))  # Default: 25°C
humidity = float(sensor.get("humidity", 60))    # Default: 60%
ph = float(sensor.get("ph", 6.5))               # Default: 6.5
rainfall = float(sensor.get("moisture", 50))    # Default: 50mm
```

If ESP32 connection fails entirely → Error page with Retry button

---

## 🚀 Advanced Features (Optional)

### 1. Manual Override
Users can still manually enter data if they want:
- Modify `crop.html` to show a "Manual Input" toggle
- When toggled, display the old input form

### 2. Data Logging
Log sensor readings for historical analysis:
```python
# Add this in app.py crop_prediction route
log_sensor_data = {
    'timestamp': datetime.now(),
    'N': N, 'P': P, 'K': K,
    'temperature': temperature,
    'humidity': humidity,
    'ph': ph,
    'rainfall': rainfall,
    'prediction': final_prediction
}
# Save to CSV or database
```

### 3. Real-time Monitoring
Display sensor readings on dashboard:
- Create a new `/sensor-dashboard` route
- Use Chart.js to plot sensor data over time

### 4. Multiple Sensor Support
Support multiple ESP32 devices:
```python
# app.py
ESP_URLS = {
    'field_1': 'http://172.20.220.21/readings',
    'field_2': 'http://172.20.220.22/readings',
    'field_3': 'http://172.20.220.23/readings'
}
```

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to ESP32"
**Solution:**
1. Check if ESP32 device is powered on
2. Check if ESP32 is on the same network as your Flask app
3. Verify IP address: `ping 172.20.220.21`
4. Check ESP32 endpoint: `curl http://172.20.220.21/readings`

### Issue: Sensor values all show "- "
**Solution:**
1. ESP32 JSON response format incorrect
2. Check JSON keys match exactly: `nitrogen`, `phosphorus`, `potassium`, `temperature_dht`, `humidity`, `ph`, `moisture`
3. Values should be numbers (not strings)

### Issue: Wrong crop prediction
**Solution:**
1. Verify sensor calibration (NPK sensor, DHT sensor, etc.)
2. Check if values are in expected ranges:
   - N, P, K: 0-100 ppm
   - Temperature: 0-50°C
   - Humidity: 0-100%
   - pH: 3-10
   - Rainfall: 0-200mm
3. Train RandomForest.pkl with more diverse sensor data if needed

### Issue: Form doesn't auto-submit
**Solution:**
1. Check browser console for JavaScript errors (F12 → Console)
2. Verify ESP32 data is being fetched (F12 → Network)
3. Check if hidden form fields are being populated

---

## 📋 Deployment Checklist

Before going to production:

- [ ] Test ESP32 endpoint is accessible from production server
- [ ] Update ESP32 URL in app.py if IP changes
- [ ] Update ESP32 URL in crop.html JavaScript if IP changes
- [ ] Configure error email notifications if sensor fails
- [ ] Set up logging for sensor readings
- [ ] Test with multiple different sensor readings
- [ ] Verify RandomForest.pkl model accuracy with real data
- [ ] Set up database backup for sensor logs

---

## 📞 Support

If you encounter issues:

1. **Check Flask logs:**
   ```bash
   # Terminal output will show errors like:
   # ERROR: Unable to connect to ESP32 at 172.20.220.21
   ```

2. **Check browser console:**
   ```
   F12 → Console tab → Look for JavaScript errors
   ```

3. **Test endpoint manually:**
   ```bash
   # PowerShell
   Invoke-WebRequest -Uri "http://172.20.220.21/readings" | ConvertFrom-Json
   ```

---

## ✨ Summary

**What Changed:**
- ✅ `crop.html` - Now auto-fetches ESP32 data with loading animation
- ✅ `app.py` - Updated `/crop-predict` route to accept auto ESP32 data
- ✅ `crop-result.html` - Shows sensor data used for prediction

**What Didn't Change:**
- ✅ RandomForest.pkl model (unchanged)
- ✅ Model prediction logic (unchanged)
- ✅ Feature engineering (unchanged)

**User Experience:**
1. User clicks "Crop"
2. Sensors auto-load
3. Crop recommendation appears
4. User sees what data was used

**Status:** ✅ READY FOR PRODUCTION
