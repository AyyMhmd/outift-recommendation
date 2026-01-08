"""
Backend Flask untuk Outfit Recommendation System
Mengintegrasikan ML model dengan Weather API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import joblib
import pickle
import pandas as pd
import numpy as np
import os
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS untuk akses dari frontend

# ===========================
# KONFIGURASI
# ===========================
WEATHER_API_KEY = "dd2f2983e1ee56f40e27570561b01446"
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Path ke model dan encoder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.join(BASE_DIR, "..", "ml")
MODEL_PATH = os.path.join(ML_DIR, "model", "multilabel_model.pkl")
ENCODERS_PATH = os.path.join(ML_DIR, "model", "encoders.pkl")
RECOMMENDER_PATH = os.path.join(ML_DIR, "model", "recommender.pkl")

# ===========================
# LOAD MODEL
# ===========================
try:
    multilabel_model = joblib.load(MODEL_PATH)
    print("✅ Multilabel model loaded successfully")
except Exception as e:
    print(f"⚠️ Could not load multilabel model: {e}")
    multilabel_model = None

try:
    with open(ENCODERS_PATH, "rb") as f:
        encoders = pickle.load(f)
    print("✅ Encoders loaded successfully")
except Exception as e:
    print(f"⚠️ Could not load encoders: {e}")
    encoders = None

# ===========================
# MAPPING DATA
# ===========================
# Mapping untuk encode input
# Mapping untuk encode input
# Keys must be lowercased for robust matching
GENDER_MAP = {
    "laki-laki": 0, "perempuan": 1, 
    "men": 0, "women": 1, "boys": 0, "girls": 1, "unisex": 0,
    "pria": 0, "wanita": 1
}

WEATHER_MAP = {
    "berawan": 0, "cerah": 1, "gerimis": 2, "hujan": 3, "mendung": 4,
    "cloudy": 0, "clear": 1, "drizzle": 2, "rain": 3, "overcast": 4,
    "clouds": 0, "rainy": 3, "sunny": 1
}

LOCATION_MAP = {
    "indoor": 0, "outdoor": 1,
    "dalam ruangan": 0, "luar ruangan": 1
}

ACTIVITY_MAP = {
    "bekerja": 0, "berjalan": 1, "kondangan": 2, "olahraga": 3, "santai": 4,
    "formal": 0, "work": 0, "office": 0,
    "walking": 1, "travel": 1, "casual": 1, 
    "party": 2, "wedding": 2,
    "sports": 3, "exercise": 3, "running": 3,
    "relax": 4, "hangout": 4, "home": 4, 
    "smart casual": 0, "ethnic": 2
}

# Mapping kota ke format OpenWeatherMap
CITY_MAP = {
    "Jakarta Pusat": "Jakarta,ID",
    "Jakarta Utara": "Jakarta,ID",
    "Jakarta Selatan": "Jakarta,ID",
    "Jakarta Barat": "Jakarta,ID",
    "Jakarta Timur": "Jakarta,ID",
    "Kepulauan Seribu": "Jakarta,ID",
    "Bogor": "Bogor,ID",
    "Depok": "Depok,ID",
    "Bekasi": "Bekasi,ID",
    "Tangerang": "Tangerang,ID",
    "Tangerang Selatan": "Tangerang,ID"
}

# Mapping weather description ke kategori
def get_weather_category(weather_desc, weather_id):
    """Konversi weather description dari API ke kategori lokal"""
    weather_desc = weather_desc.lower()
    
    # Berdasarkan weather ID dari OpenWeatherMap
    if weather_id >= 200 and weather_id < 300:  # Thunderstorm
        return "hujan"
    elif weather_id >= 300 and weather_id < 400:  # Drizzle
        return "gerimis"
    elif weather_id >= 500 and weather_id < 600:  # Rain
        return "hujan"
    elif weather_id >= 600 and weather_id < 700:  # Snow
        return "hujan"  # Treat as rain for Indonesia
    elif weather_id >= 700 and weather_id < 800:  # Atmosphere (mist, fog, etc)
        return "mendung"
    elif weather_id == 800:  # Clear
        return "cerah"
    elif weather_id > 800:  # Clouds
        if weather_id == 801:  # Few clouds
            return "cerah"
        elif weather_id == 802:  # Scattered clouds
            return "berawan"
        else:  # Broken/overcast clouds
            return "mendung"
    
    return "berawan"  # Default

# ===========================
# HELPER FUNCTIONS
# ===========================
def get_location():
    """Detect location based on IP address"""
    try:
        response = requests.get("http://ip-api.com/json/", timeout=5)
        data = response.json()
        if data["status"] == "success":
            return data["city"]
        else:
            print("Failed to detect location, defaulting to Jakarta.")
            return "Jakarta"
    except Exception as e:
        print(f"Error detecting location: {e}")
        return "Jakarta"

def get_weather_data(city=None, lat=None, lon=None):
    """Ambil data cuaca dari OpenWeatherMap API"""
    params = {
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "id"
    }

    if lat and lon:
        print(f"DEBUG: Fetching weather for coordinates: {lat}, {lon}")
        params["lat"] = lat
        params["lon"] = lon
    else:
        # Auto-detect location if nothing provided
        if not city:
            city = get_location()
        
        city_query = CITY_MAP.get(city, f"{city},ID")
        # print(f"DEBUG: Fetching weather for city: {city_query}")
        params["q"] = city_query
    
    try:
        response = requests.get(WEATHER_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        weather_id = data["weather"][0]["id"]
        weather_desc = data["weather"][0]["description"]
        
        return {
            "temperature": round(data["main"]["temp"]),
            "humidity": data["main"]["humidity"],
            "weather_desc": weather_desc,
            "weather_category": get_weather_category(weather_desc, weather_id),
            "feels_like": round(data["main"]["feels_like"]),
            "city": data["name"],
            "icon": data["weather"][0]["icon"]
        }
    except requests.exceptions.RequestException as e:
        print(f"Weather API error: {e}")
        # Return default data jika API gagal
        return {
            "temperature": 28,
            "humidity": 75,
            "weather_desc": "berawan",
            "weather_category": "berawan",
            "feels_like": 30,
            "city": city if city else "Jakarta",
            "icon": "03d"
        }

def determine_location(activity, subcategory):
    """Tentukan lokasi berdasarkan aktivitas dan kategori"""
    outdoor_activities = ["olahraga", "berjalan", "sports"]
    outdoor_subcategories = ["swimwear", "tracksuits"]
    
    if activity.lower() in outdoor_activities:
        return "outdoor"
    if subcategory.lower() in outdoor_subcategories:
        return "outdoor"
    return "indoor"

def map_activity(usage, subcategory):
    """Map usage ke activity yang sesuai dengan model"""
    usage_lower = usage.lower()
    
    activity_mapping = {
        "casual": "santai",
        "formal": "bekerja",
        "sports": "olahraga",
        "ethnic": "kondangan",
        "smart casual": "bekerja",
        "party": "kondangan",
        "travel": "berjalan"
    }
    
    return activity_mapping.get(usage_lower, "santai")

def predict_outfit(input_data):
    """Prediksi outfit menggunakan multilabel model"""
    if multilabel_model is None:
        # Fallback jika model tidak tersedia
        return get_fallback_recommendation(input_data)
    
    try:
        # Prepare input features sesuai dengan X_multilabel.csv
        # Columns: gender, weather, temperature, humidity, location, activity, duration
        
        gender_val = input_data["gender"]
        if isinstance(gender_val, str):
            gender = GENDER_MAP.get(gender_val.lower(), 0)
        else:
            gender = gender_val

        weather_val = input_data["weather_category"]
        # weather_category from API might be different than our map keys if not normalized
        if isinstance(weather_val, str):
             weather = WEATHER_MAP.get(weather_val.lower(), 0)
        else:
             weather = weather_val

        temperature = input_data["temperature"]
        humidity = input_data["humidity"]
        
        location_val = input_data["location"]
        if isinstance(location_val, str):
            location = LOCATION_MAP.get(location_val.lower(), 0)
        else:
            location = location_val
            
        activity_val = input_data["activity"]
        if isinstance(activity_val, str):
             activity = ACTIVITY_MAP.get(activity_val.lower(), 4)
        else:
             activity = activity_val
             
        duration = 12  # Default duration
        
        # Create DataFrame dengan kolom yang sesuai
        X = pd.DataFrame([[gender, weather, temperature, humidity, location, activity, duration]],
                        columns=["gender", "weather", "temperature", "humidity", "location", "activity", "duration"])
        
        # Predict
        predictions = multilabel_model.predict(X)
        
        # Decode predictions (untuk multilabel, output adalah binary array)
        return decode_predictions(predictions[0], input_data)
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return get_fallback_recommendation(input_data)

def decode_predictions(predictions, input_data):
    """Decode binary predictions ke outfit recommendations"""
    
    # Get output encoder (MultiLabelBinarizer)
    if isinstance(encoders, dict) and "output_encoder" in encoders:
        mlb = encoders["output_encoder"]
        classes = mlb.classes_
    else:
        # Fallback if encoders structure is different
        print("⚠️ Warning: Output encoder not found or invalid format")
        return get_fallback_recommendation(input_data)

    # Get predicted items directly from the binary vector
    predicted_items = []
    for idx, is_present in enumerate(predictions):
        if is_present == 1:
            predicted_items.append(classes[idx])
            
    # print(f"DEBUG: Model predicted raw items: {predicted_items}")
    
    # Categorize items
    recommendations = {
        "top": {"type": "none", "name": "Tidak diperlukan"},
        "bottom": {"type": "none", "name": "Tidak diperlukan"},
        "outerwear": {"type": "none", "name": "Tidak diperlukan"},
        "footwear": {"type": "none", "name": "Tidak diperlukan"}
    }
    
    # Mapping item types to categories
    # Note: These keys must match the labels in mlb.classes_
    item_categories = {
        "kaos": "top", "kemeja": "top", "blouse": "top", "jas": "top", 
        "tank top": "top", "kaos olahraga": "top", "atasan formal": "top", "kebaya": "top",
        "sweater": "top", "jersey": "top",
        
        "celana panjang": "bottom", "celana pendek": "bottom", "rok": "bottom", 
        "legging": "bottom", "celana olahraga": "bottom", "jeans": "bottom", 
        "chino": "bottom", "celana bahan": "bottom", "celana formal": "bottom",
        
        "jaket": "outerwear", "hoodie": "outerwear", "cardigan": "outerwear",
        "jaket waterproof": "outerwear", "raincoat": "outerwear", "jaket ringan": "outerwear",
        "jaket tipis": "outerwear", "tanpa pakaian luar": "outerwear",
        
        "sneakers": "footwear", "sepatu bot": "footwear", "sepatu pantofel": "footwear", 
        "sepatu hak": "footwear", "sandal": "footwear", "running shoes": "footwear",
        "boots": "footwear", "sepatu waterproof": "footwear", "flat shoes": "footwear",
        "wedges": "footwear", "loafers": "footwear", "casual shoes": "footwear"
    }

    found_categories = set()
    
    for item in predicted_items:
        # Check standard category map
        category = item_categories.get(item)
        
        # Heuristic checks if item not in map (e.g. typos or variations)
        if not category:
            if "celana" in item or "rok" in item: category = "bottom"
            elif "jaket" in item or "hoodie" in item: category = "outerwear"
            elif "sepatu" in item or "sandal" in item: category = "footwear"
            elif "kaos" in item or "kemeja" in item: category = "top"
        
        if category and category not in found_categories:
            recommendations[category] = {
                "name": item.title(),
                "type": item,
                "confidence": 85, # Default confidence for now
                "reason": f"Disarankan oleh AI untuk aktivitas {input_data.get('activity', '')}"
            }
            found_categories.add(category)
            
    # If key categories missing, fallback to smart recommendations for those specific slots?
    # Or just return what the model predicted. 
    # Let's keep it strict to the model for now, but ensure 'none' is handled.
    
    return recommendations

def filter_recommendations(recommendations, input_data):
    """
    Filter heuristic untuk memperbaiki hasil prediksi yang tidak masuk akal.
    Rules:
    1. Temp > 28°C & !Hujan -> Remove Heavy Outerwear
    2. Activity = Olahraga -> Prioritize Sportswear
    3. Activity = Formal -> Remove Casual items (Shorts, Sandals)
    """
    filtered = recommendations.copy()
    
    # Extract conditions
    temp = input_data.get("temperature", 25)
    weather_cat = input_data.get("weather_category", 0) # 0=berawan, 1=cerah, 3=hujan
    activity = input_data.get("activity", 4) # 4=Santai, 3=Olahraga, 0=Bekerja
    
    # --- RULE 1: HEAT CHECK ---
    # Jika panas (>28C) dan tidak hujan (3), hapus jaket tebal
    should_remove_outerwear = False
    if temp > 28 and weather_cat != 3: 
        should_remove_outerwear = True
        
    if should_remove_outerwear:
        outer = filtered.get("outerwear", {})
        if outer.get("type") in ["jaket", "hoodie", "coat", "sweater", "blazer", "cardigan"]:
            print(f"DEBUG: Removing outerwear '{outer.get('name')}' due to heat ({temp}C)")
            filtered["outerwear"] = {"type": "none", "name": "Tidak diperlukan"}

    # --- RULE 2: SPORT CHECK ---
    # Jika olahraga (3), pastikan footwear bukan pantofel/hak
    if activity == 3: 
        foot = filtered.get("footwear", {})
        if foot.get("type") in ["sepatu pantofel", "sepatu hak", "boots", "loafers"]:
            print(f"DEBUG: Replacing footwear '{foot.get('name')}' for sports")
            filtered["footwear"] = {
                "name": "Running Shoes", 
                "type": "running shoes", 
                "confidence": 95, 
                "reason": "Wajib untuk olahraga"
            }
            
        # Pastikan tidak pakai jeans/chino
        bottom = filtered.get("bottom", {})
        if bottom.get("type") in ["jeans", "chino", "celana bahan", "rok"]:
             print(f"DEBUG: Replacing bottom '{bottom.get('name')}' for sports")
             filtered["bottom"] = {
                 "name": "Celana Olahraga",
                 "type": "celana olahraga",
                 "confidence": 95,
                 "reason": "Nyaman untuk bergerak"
             }

    # --- RULE 3: FORMAL CHECK ---
    # Jika bekerja (0) atau kondangan (2)
    if activity in [0, 2]:
        # No shorts
        bottom = filtered.get("bottom", {})
        if bottom.get("type") in ["celana pendek", "panty", "hotpants"]:
            gender = input_data.get("gender", 0)
            new_bottom = "Celana Bahan" if gender == 0 else "Rok/Celana Bahan"
            new_type = "celana bahan"
            
            print(f"DEBUG: Replacing casual bottom '{bottom.get('name')}' for formal")
            filtered["bottom"] = {
                "name": new_bottom,
                "type": new_type,
                "confidence": 90,
                "reason": "Sopan untuk formal"
            }
            
        # No flip-flops/sandals (unless wanita & cantik? but generally no jepit)
        foot = filtered.get("footwear", {})
        if foot.get("type") in ["sandal", "flip flops", "crocs"]:
             print(f"DEBUG: Replacing casual footwear '{foot.get('name')}' for formal")
             filtered["footwear"] = {
                 "name": "Sepatu Tertutup",
                 "type": "sepatu pantofel",
                 "confidence": 90,
                 "reason": "Formal look"
             }

    return filtered

def generate_smart_recommendations(weather_category, temperature, activity, gender):
    """Generate smart outfit recommendations berdasarkan kondisi"""
    
    recommendations = {
        "top": {},
        "bottom": {},
        "outerwear": {},
        "footwear": {}
    }
    
    # === TOP ===
    if activity == "kondangan":
        if gender in ["perempuan", "women", "girls"]:
            recommendations["top"] = {
                "name": "Blouse Elegan",
                "type": "blouse",
                "confidence": 90,
                "reason": "Cocok untuk acara formal"
            }
        else:
            recommendations["top"] = {
                "name": "Kemeja Formal",
                "type": "kemeja",
                "confidence": 92,
                "reason": "Tampil rapi untuk acara formal"
            }
    elif activity == "bekerja":
        recommendations["top"] = {
            "name": "Kemeja Kerja",
            "type": "kemeja",
            "confidence": 88,
            "reason": "Profesional untuk bekerja"
        }
    elif activity == "olahraga":
        recommendations["top"] = {
            "name": "Kaos Olahraga",
            "type": "kaos",
            "confidence": 95,
            "reason": "Nyaman untuk bergerak"
        }
    elif temperature > 30:
        recommendations["top"] = {
            "name": "Kaos Ringan",
            "type": "kaos",
            "confidence": 87,
            "reason": f"Cuaca panas ({temperature}°C)"
        }
    else:
        recommendations["top"] = {
            "name": "Kemeja Casual",
            "type": "kemeja",
            "confidence": 85,
            "reason": "Versatile untuk berbagai aktivitas"
        }
    
    # === BOTTOM ===
    if activity == "olahraga":
        if gender in ["perempuan", "women", "girls"]:
            recommendations["bottom"] = {
                "name": "Legging",
                "type": "legging",
                "confidence": 93,
                "reason": "Fleksibel untuk olahraga"
            }
        else:
            recommendations["bottom"] = {
                "name": "Celana Olahraga",
                "type": "celana olahraga",
                "confidence": 93,
                "reason": "Nyaman untuk aktivitas fisik"
            }
    elif activity == "kondangan":
        if gender in ["perempuan", "women", "girls"]:
            recommendations["bottom"] = {
                "name": "Rok Elegan",
                "type": "rok",
                "confidence": 88,
                "reason": "Tampilan feminin untuk acara formal"
            }
        else:
            recommendations["bottom"] = {
                "name": "Celana Bahan",
                "type": "celana panjang",
                "confidence": 90,
                "reason": "Formal dan rapi"
            }
    elif temperature > 32:
        recommendations["bottom"] = {
            "name": "Celana Pendek",
            "type": "celana pendek",
            "confidence": 86,
            "reason": f"Sejuk di cuaca panas ({temperature}°C)"
        }
    else:
        recommendations["bottom"] = {
            "name": "Celana Panjang",
            "type": "celana panjang",
            "confidence": 85,
            "reason": "Cocok untuk berbagai situasi"
        }
    
    # === OUTERWEAR ===
    if weather_category == "hujan":
        recommendations["outerwear"] = {
            "name": "Jaket Waterproof",
            "type": "jaket",
            "confidence": 95,
            "reason": "Melindungi dari hujan"
        }
    elif weather_category == "gerimis":
        recommendations["outerwear"] = {
            "name": "Jaket Ringan",
            "type": "jaket",
            "confidence": 88,
            "reason": "Proteksi dari gerimis"
        }
    elif temperature < 25:
        recommendations["outerwear"] = {
            "name": "Hoodie",
            "type": "hoodie",
            "confidence": 82,
            "reason": f"Hangatkan di suhu {temperature}°C"
        }
    elif weather_category == "mendung":
        recommendations["outerwear"] = {
            "name": "Cardigan",
            "type": "hoodie",
            "confidence": 70,
            "reason": "Jaga-jaga cuaca berubah"
        }
    else:
        recommendations["outerwear"] = {
            "name": "Tanpa Outerwear",
            "type": "none",
            "confidence": 75,
            "reason": f"Cuaca cerah ({temperature}°C)"
        }
    
    # === FOOTWEAR ===
    if weather_category in ["hujan", "gerimis"]:
        recommendations["footwear"] = {
            "name": "Sepatu Boot",
            "type": "sepatu bot",
            "confidence": 92,
            "reason": "Tahan air dan nyaman"
        }
    elif activity == "kondangan":
        if gender in ["perempuan", "women", "girls"]:
            recommendations["footwear"] = {
                "name": "Sepatu Hak",
                "type": "sepatu hak",
                "confidence": 88,
                "reason": "Elegan untuk acara formal"
            }
        else:
            recommendations["footwear"] = {
                "name": "Sepatu Pantofel",
                "type": "sepatu pantofel",
                "confidence": 90,
                "reason": "Formal dan berkelas"
            }
    elif activity in ["santai"]:
        recommendations["footwear"] = {
            "name": "Sandal",
            "type": "sandal",
            "confidence": 85,
            "reason": "Nyaman untuk santai"
        }
    else:
        recommendations["footwear"] = {
            "name": "Sneakers",
            "type": "sneakers",
            "confidence": 90,
            "reason": "Versatile dan nyaman"
        }
    
    return recommendations

def get_fallback_recommendation(input_data):
    """Fallback recommendation jika model tidak tersedia"""
    return generate_smart_recommendations(
        input_data.get("weather_category", "berawan"),
        input_data.get("temperature", 28),
        input_data.get("activity", "santai"),
        input_data.get("gender", "").lower()
    )

def get_outfit_image(outfit_type):
    """Get image URL untuk outfit type"""
    image_map = {
        "kaos": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300",
        "kemeja": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=300",
        "blouse": "https://images.unsplash.com/photo-1564257631407-4deb1f99d992?w=300",
        "jas": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=300",
        "celana panjang": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=300",
        "celana pendek": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=300",
        "celana olahraga": "https://images.unsplash.com/photo-1556906781-9a412961c28c?w=300",
        "rok": "https://images.unsplash.com/photo-1583496661160-fb5886a0uj7e?w=300",
        "legging": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=300",
        "jaket": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=300",
        "hoodie": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=300",
        "none": "",
        "sneakers": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300",
        "sepatu bot": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=300",
        "sepatu pantofel": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=300",
        "sepatu hak": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=300",
        "sandal": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300"
    }
    return image_map.get(outfit_type, "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=300")

# ===========================
# API ENDPOINTS
# ===========================

@app.route("/")
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "message": "Outfit Recommendation API is running",
        "version": "1.0.0"
    })

@app.route("/api/weather", methods=["GET"])
def get_weather():
    """Get weather data untuk kota tertentu atau koordinat"""
    city = request.args.get("city")
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    
    weather_data = get_weather_data(city=city, lat=lat, lon=lon)
    return jsonify(weather_data)

@app.route("/api/recommend", methods=["POST"])
def recommend_outfit():
    """Main endpoint untuk rekomendasi outfit"""
    try:
        data = request.get_json()
        
        # Required fields
        gender = data.get("gender", "")
        subcategory = data.get("subcategory", "")
        article_type = data.get("articleType", "")
        base_colour = data.get("baseColour", "")
        usage = data.get("usage", "casual")
        season = data.get("season", "summer")
        city = data.get("city")
        lat = data.get("lat")
        lon = data.get("lon")
        
        # Get weather data
        weather_data = get_weather_data(city=city, lat=lat, lon=lon)
        
        # Map usage ke activity
        activity = map_activity(usage, subcategory)
        
        # Determine location
        location = determine_location(activity, subcategory)
        
        # Prepare input untuk prediksi
        # Normalize and map inputs
        gender_norm = str(gender).lower().strip()
        usage_norm = str(usage).lower().strip()
        activity_norm = str(activity).lower().strip()
        
        # Override activity from map if possible
        mapped_activity = ACTIVITY_MAP.get(usage_norm) or ACTIVITY_MAP.get(activity_norm) or 4 # Default santai
        
        # Override gender from map
        mapped_gender = GENDER_MAP.get(gender_norm, 0) # Default laki-laki
        
        # Override location from map if passed string
        # location might be int (0/1) or string ("indoor"/"outdoor")
        location_norm = str(location).lower().strip()
        # If it's already "0" or "none", map it safely
        if location_norm == "0": mapped_location = 0
        elif location_norm == "1": mapped_location = 1
        else: mapped_location = LOCATION_MAP.get(location_norm, 1) # Default outdoor
        
        # Weather map
        weather_cat_norm = str(weather_data["weather_category"]).lower()
        mapped_weather = WEATHER_MAP.get(weather_cat_norm, 0)

        print(f"DEBUG: Input Processing:")
        print(f"  Gender: '{gender}' -> '{gender_norm}' -> {mapped_gender}")
        print(f"  Usage: '{usage}' -> Activity Map: {ACTIVITY_MAP.get(usage_norm)}")
        print(f"  Final Activity: {mapped_activity}")
        print(f"  Weather: '{weather_cat_norm}' -> {mapped_weather}")

        input_data = {
            "gender": mapped_gender,
            "subcategory": subcategory, # Not used by model based on previous analysis, but kept
            "article_type": article_type, # Not used
            "base_colour": base_colour, # Not used
            "usage": usage, # Mapped to activity
            "season": season, # Not explicitly used by model input based on inspect_model output
            "activity": mapped_activity,
            "location": mapped_location,
            "temperature": weather_data["temperature"],
            "humidity": weather_data["humidity"],
            "weather_category": mapped_weather # Used for model consistency? Model trained on integer categories
        }
        
        # Get recommendations
        recommendations = predict_outfit(input_data)
        
        # Apply Smart Filters (Heuristics)
        recommendations = filter_recommendations(recommendations, input_data)
        
        # Format response dengan image URLs
        formatted_recommendations = []
        for category, rec in recommendations.items():
            if rec.get("type") != "none":
                formatted_recommendations.append({
                    "category": category,
                    "name": rec.get("name", ""),
                    "type": rec.get("type", ""),
                    "confidence": rec.get("confidence", 80),
                    "reason": rec.get("reason", ""),
                    "image": get_outfit_image(rec.get("type", ""))
                })
            else:
                formatted_recommendations.append({
                    "category": category,
                    "name": rec.get("name", "Tidak diperlukan"),
                    "type": "none",
                    "confidence": rec.get("confidence", 75),
                    "reason": rec.get("reason", ""),
                    "image": ""
                })
        
        return jsonify({
            "success": True,
            "weather": weather_data,
            "input": {
                "gender": gender,
                "usage": usage,
                "activity": activity,
                "season": season,
                "city": city,
                "mapped_activity": mapped_activity, 
                "mapped_weather": mapped_weather
            },
            "recommendations": formatted_recommendations
        })
        
    except Exception as e:
        print(f"Error in recommend_outfit: {e}")
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/api/options", methods=["GET"])
def get_options():
    """Get all dropdown options untuk frontend"""
    return jsonify({
        "gender": ["Men", "Women", "Boys", "Girls", "Unisex"],
        "subcategory": [
            "apparel set", "bottomwear", "dress", "innerwear",
            "loungewear and nightwear", "saree", "socks", "topwear"
        ],
        "usage": ["casual", "ethnic", "formal", "sports", "smart casual", "party", "travel"],
        "season": ["fall", "summer", "winter", "spring"],
        "cities": [
            "Jakarta Pusat", "Jakarta Utara", "Jakarta Selatan",
            "Jakarta Barat", "Jakarta Timur", "Kepulauan Seribu",
            "Bogor", "Depok", "Bekasi", "Tangerang", "Tangerang Selatan"
        ]
    })

# ===========================
# RUN SERVER
# ===========================
if __name__ == "__main__":
    print("🚀 Starting Outfit Recommendation Backend...")
    print(f"📁 ML Model Path: {MODEL_PATH}")
    print(f"🌐 Weather API: OpenWeatherMap")
    app.run(host="0.0.0.0", port=5000, debug=True)
