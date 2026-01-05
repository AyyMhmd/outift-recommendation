# 🚀 Backend - Outfit Recommendation System

Backend API untuk sistem rekomendasi outfit berbasis cuaca dan preferensi pengguna.

## 📋 Prerequisites

- Python 3.8 atau lebih baru
- pip (Python package manager)

## 🛠️ Instalasi

1. **Masuk ke folder backend:**

   ```bash
   cd backend
   ```

2. **Buat virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # atau
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Menjalankan Server

```bash
python app.py
```

Server akan berjalan di `http://localhost:5000`

## 📡 API Endpoints

### 1. Health Check

```
GET /
```

Response:

```json
{
  "status": "ok",
  "message": "Outfit Recommendation API is running",
  "version": "1.0.0"
}
```

### 2. Get Weather Data

```
GET /api/weather?city=Jakarta
```

Response:

```json
{
  "temperature": 28,
  "humidity": 75,
  "weather_desc": "berawan",
  "weather_category": "berawan",
  "feels_like": 30,
  "city": "Jakarta",
  "icon": "03d"
}
```

### 3. Get Outfit Recommendations

```
POST /api/recommend
Content-Type: application/json

{
  "gender": "Women",
  "subcategory": "topwear",
  "articleType": "shirts",
  "baseColour": "blue",
  "usage": "casual",
  "season": "summer",
  "city": "Jakarta Selatan"
}
```

Response:

```json
{
  "success": true,
  "weather": {...},
  "input": {...},
  "recommendations": [
    {
      "category": "top",
      "name": "Kaos Ringan",
      "type": "kaos",
      "confidence": 87,
      "reason": "Cuaca panas (28°C)",
      "image": "https://..."
    },
    ...
  ]
}
```

### 4. Get Options

```
GET /api/options
```

Response: Semua opsi dropdown untuk frontend

## 🌐 Weather API

Backend menggunakan **OpenWeatherMap API** untuk mendapatkan data cuaca real-time.

API Key sudah dikonfigurasi di file `.env`

## 📁 Struktur File

```
backend/
├── app.py           # Main Flask application
├── utils.py         # Helper functions
├── requirements.txt # Python dependencies
├── .env             # Environment variables
└── README.md        # Dokumentasi ini
```

## 🔧 Konfigurasi

Edit file `.env` untuk mengubah konfigurasi:

```env
OPENWEATHER_API_KEY=your_api_key_here
FLASK_ENV=development
PORT=5000
```

## 🧪 Testing

Gunakan curl atau Postman:

```bash
# Test health check
curl http://localhost:5000/

# Test weather
curl "http://localhost:5000/api/weather?city=Jakarta"

# Test recommendation
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"gender":"Women","city":"Jakarta","usage":"casual"}'
```

## 📝 Notes

- Backend harus berjalan agar frontend dapat berfungsi
- CORS sudah diaktifkan untuk akses dari frontend
- Model ML akan dimuat otomatis dari folder `ml/model/`
