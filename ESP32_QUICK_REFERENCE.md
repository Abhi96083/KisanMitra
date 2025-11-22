# ESP32 Integration - Quick Reference

## 🎯 What Was Done

Your Flask app now **automatically reads sensor data from ESP32** and predicts crop recommendations.

---

## 📡 How It Works (Simple Version)

```
1. User clicks "Crop" button
   ↓
2. Page shows "Fetching ESP32 Sensor Data..."
   ↓
3. Sensor values display (N, P, K, Temp, Humidity, pH, Moisture)
   ↓
4. Page automatically shows: "Recommended Crop: Rice" (or similar)
   ↓
5. User sees which sensor values were used
```

---

## 🔧 Configuration (If IP Changes)

**ESP32 IP Address:** `172.20.220.21`

If this changes, update TWO files:

### 1. **app/app.py** (Line ~24)
```python
ESP_URL = "http://172.20.220.21/readings"  # ← Change this
```

### 2. **app/templates/crop.html** (Line ~83)
```javascript
fetch('http://172.20.220.21/readings')  // ← And this
```

---

## ✅ Files Changed

| File | What Changed | Why |
|---|---|---|
| `app/app.py` | `/crop-predict` route | Now handles auto ESP32 data + passes sensor values to display |
| `app/templates/crop.html` | Entire page | Shows loading → sensor data → auto-submit |
| `app/templates/crop-result.html` | Added sensor table | Display all sensor values used |

---

## ❌ What Did NOT Change

- ✅ RandomForest.pkl model
- ✅ Model prediction function
- ✅ ML algorithm
- ✅ Disease detection
- ✅ Fertilizer recommendation
- ✅ Any other feature

**Only the CROP PREDICTION input method changed from manual to automatic.**

---

## 🧪 Quick Test

1. Start Flask app:
   ```bash
   cd c:\Users\mnkp9\Kishanmitra
   python -m flask run --app app.app
   ```

2. Open browser: `http://localhost:5000`

3. Click "Crop" in navbar

4. You should see:
   - Loading message
   - All 7 sensor values
   - Recommended crop appears
   - Sensor data table on results page

---

## 🚨 If It Doesn't Work

### Error: "Cannot connect to ESP32"
- ✅ Is ESP32 powered on?
- ✅ Is it on same network?
- ✅ Is IP `172.20.220.21` correct?
- ✅ Test: `ping 172.20.220.21`

### Loading spinner never goes away
- ✅ Check browser F12 → Console for errors
- ✅ Check Network tab - is ESP32 responding?
- ✅ Is ESP32 JSON response valid?

### Shows error "Sensor Connection Error"
- ✅ ESP32 is offline or unreachable
- ✅ Click "Retry" button
- ✅ Or turn on ESP32 and try again

---

## 📊 Sensor Data Format

ESP32 should return JSON like this:

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

**Key names MUST match exactly** (including `_dht` for temperature)

---

## 🎨 User Experience

### Before:
```
1. User clicks "Crop"
2. Form with 7 input boxes appears
3. User manually types numbers
4. User clicks "Predict" button
5. Wait for result
6. Only crop name shown
```

### After:
```
1. User clicks "Crop"
2. Loading animation appears
3. Sensor values auto-display
4. 2 seconds later → crop result appears
5. All sensor data shown in results
```

**Less work for user, more transparent results!**

---

## 📋 Sensor Data Used

| Sensor | Value | Unit |
|---|---|---|
| Nitrogen | From ESP32 | ppm |
| Phosphorus | From ESP32 | ppm |
| Potassium | From ESP32 | ppm |
| Temperature | From DHT sensor | °C |
| Humidity | From DHT sensor | % |
| pH | From pH sensor | - |
| Moisture | From soil sensor | mm |

**All 7 parameters used by RandomForest model for prediction**

---

## 🔄 Fallback Values

If ESP32 doesn't return a value, these defaults are used:

```python
nitrogen = 20         # ppm
phosphorus = 10       # ppm
potassium = 30        # ppm
temperature = 25      # °C
humidity = 60         # %
pH = 6.5              # -
moisture = 50         # mm
```

This ensures app works even if one sensor fails.

---

## 🌍 Multilingual Support

- ✅ Works in English
- ✅ Works in Hindi
- ✅ Works in Kannada
- ✅ Language selector in navbar

Note: Loading messages are in English (system messages), but crop names and results adapt to selected language.

---

## 🚀 Quick Commands

### Test ESP32 Endpoint
```bash
# PowerShell
Invoke-WebRequest -Uri "http://172.20.220.21/readings" | ConvertFrom-Json
```

### Start Flask App
```bash
cd c:\Users\mnkp9\Kishanmitra
python -m flask run --app app.app --debug
```

### Check Flask Logs
```
Look at terminal output while using app
Errors will display there
```

---

## 🎓 Learning Path

1. **Understand flow**: Read this file
2. **See changes**: Open `ESP32_CHANGES_SUMMARY.md`
3. **Test locally**: Follow `ESP32_AUTO_INTEGRATION_GUIDE.md`
4. **Troubleshoot**: Use troubleshooting section above
5. **Customize**: Modify ESP32 endpoint if needed

---

## ✨ Benefits

✅ **Automated** - No manual data entry  
✅ **Accurate** - Sensor data, not guesses  
✅ **Transparent** - See sensor values in results  
✅ **Reliable** - Error handling if sensor offline  
✅ **Unchanged** - ML model untouched  
✅ **Fast** - 2-3 seconds from click to result  

---

## 📞 Common Questions

**Q: Why do I need ESP32?**  
A: For automatic sensor-based crop recommendations without user input.

**Q: Can I still enter values manually?**  
A: Currently no (auto-fetch only). Can add manual mode if needed.

**Q: What if ESP32 goes offline?**  
A: App shows error message with "Retry" button. Uses default values if needed.

**Q: Does this change the ML model?**  
A: No. Only how data is collected - model prediction logic is identical.

**Q: What are the sensor values used for?**  
A: As input to RandomForest model to predict which crop is best.

---

**Status: ✅ READY TO USE**

For detailed documentation, see:
- `ESP32_AUTO_INTEGRATION_GUIDE.md` (detailed guide)
- `ESP32_CHANGES_SUMMARY.md` (technical changes)
