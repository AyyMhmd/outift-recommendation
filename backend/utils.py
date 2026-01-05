"""
Utility functions untuk Backend Outfit Recommendation
"""

import os
import json
from datetime import datetime

# ===========================
# CONSTANTS
# ===========================

# Mapping gender
GENDER_MAPPING = {
    "men": "laki-laki",
    "women": "perempuan",
    "boys": "laki-laki",
    "girls": "perempuan",
    "unisex": "laki-laki",
    "laki-laki": "laki-laki",
    "perempuan": "perempuan"
}

# Mapping usage ke activity
USAGE_TO_ACTIVITY = {
    "casual": "santai",
    "formal": "bekerja",
    "sports": "olahraga",
    "ethnic": "kondangan",
    "smart casual": "bekerja",
    "party": "kondangan",
    "travel": "berjalan"
}

# Weather categories
WEATHER_CATEGORIES = {
    "clear": "cerah",
    "clouds": "berawan",
    "rain": "hujan",
    "drizzle": "gerimis",
    "thunderstorm": "hujan",
    "mist": "mendung",
    "fog": "mendung",
    "haze": "mendung"
}

# Season mapping
SEASON_MAPPING = {
    "summer": {"temp_min": 28, "temp_max": 35, "humidity_avg": 70},
    "winter": {"temp_min": 15, "temp_max": 25, "humidity_avg": 80},
    "spring": {"temp_min": 22, "temp_max": 30, "humidity_avg": 65},
    "fall": {"temp_min": 20, "temp_max": 28, "humidity_avg": 75}
}

# ===========================
# HELPER FUNCTIONS
# ===========================

def normalize_gender(gender):
    """Normalize gender input ke format model"""
    return GENDER_MAPPING.get(gender.lower(), "laki-laki")

def get_activity_from_usage(usage):
    """Convert usage ke activity untuk model"""
    return USAGE_TO_ACTIVITY.get(usage.lower(), "santai")

def get_weather_category(weather_main):
    """Convert weather main ke kategori lokal"""
    return WEATHER_CATEGORIES.get(weather_main.lower(), "berawan")

def calculate_comfort_index(temperature, humidity):
    """
    Calculate comfort index berdasarkan temperature dan humidity
    Heat Index formula (simplified)
    """
    if temperature < 27:
        return "nyaman"
    
    hi = temperature + 0.5 * humidity / 10
    
    if hi < 30:
        return "nyaman"
    elif hi < 35:
        return "agak panas"
    elif hi < 40:
        return "panas"
    else:
        return "sangat panas"

def get_season_from_month(month=None):
    """
    Get season berdasarkan bulan (untuk Indonesia, musim hujan/kemarau)
    """
    if month is None:
        month = datetime.now().month
    
    # Indonesia: Musim hujan (Oct-Mar), Kemarau (Apr-Sep)
    if month in [10, 11, 12, 1, 2, 3]:
        return "rainy"  # Musim hujan
    else:
        return "dry"  # Musim kemarau

def format_outfit_response(recommendations, weather_data, input_data):
    """
    Format response untuk frontend
    """
    return {
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "weather": {
            "temperature": weather_data.get("temperature"),
            "humidity": weather_data.get("humidity"),
            "description": weather_data.get("weather_desc"),
            "category": weather_data.get("weather_category"),
            "city": weather_data.get("city"),
            "comfort": calculate_comfort_index(
                weather_data.get("temperature", 28),
                weather_data.get("humidity", 70)
            )
        },
        "input_summary": {
            "gender": input_data.get("gender"),
            "activity": input_data.get("activity"),
            "usage": input_data.get("usage"),
            "season": input_data.get("season")
        },
        "recommendations": recommendations
    }

def validate_input(data):
    """
    Validate input data dari request
    Returns: (is_valid, error_message)
    """
    required_fields = ["gender", "city"]
    
    for field in required_fields:
        if not data.get(field):
            return False, f"Field '{field}' is required"
    
    # Validate gender
    valid_genders = ["men", "women", "boys", "girls", "unisex", "laki-laki", "perempuan"]
    if data.get("gender", "").lower() not in valid_genders:
        return False, "Invalid gender value"
    
    return True, None

def get_outfit_tips(weather_category, temperature, activity):
    """
    Get additional tips berdasarkan kondisi
    """
    tips = []
    
    if weather_category == "hujan":
        tips.append("💡 Bawa payung atau jas hujan")
        tips.append("💡 Hindari pakaian berbahan cotton yang mudah basah")
    
    if temperature > 32:
        tips.append("💡 Pilih pakaian berbahan ringan dan breathable")
        tips.append("💡 Gunakan sunscreen saat beraktivitas outdoor")
    
    if temperature < 22:
        tips.append("💡 Layer pakaian untuk menjaga kehangatan")
    
    if activity == "olahraga":
        tips.append("💡 Pilih pakaian dengan teknologi quick-dry")
        tips.append("💡 Jangan lupa bawa air minum")
    
    if activity == "kondangan":
        tips.append("💡 Perhatikan dress code acara")
        tips.append("💡 Hindari warna putih jika menghadiri pernikahan")
    
    return tips

def log_recommendation(input_data, recommendations):
    """
    Log recommendation untuk analytics (optional)
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "input": input_data,
        "output_count": len(recommendations)
    }
    
    # Bisa disimpan ke file atau database
    # Untuk sekarang, hanya print
    print(f"[LOG] Recommendation: {json.dumps(log_entry)}")

# ===========================
# OUTFIT CATEGORY HELPERS
# ===========================

def get_top_options(activity, temperature, gender):
    """Get top outfit options"""
    options = {
        "kondangan": {
            "perempuan": ["blouse", "kebaya", "atasan formal"],
            "laki-laki": ["kemeja", "batik", "jas"]
        },
        "bekerja": {
            "perempuan": ["kemeja", "blouse"],
            "laki-laki": ["kemeja", "polo"]
        },
        "olahraga": {
            "perempuan": ["kaos olahraga", "tank top"],
            "laki-laki": ["kaos olahraga", "jersey"]
        },
        "santai": {
            "perempuan": ["kaos", "blouse casual"],
            "laki-laki": ["kaos", "kemeja casual"]
        },
        "berjalan": {
            "perempuan": ["kaos", "kemeja"],
            "laki-laki": ["kaos", "kemeja"]
        }
    }
    
    gender_key = normalize_gender(gender)
    return options.get(activity, options["santai"]).get(gender_key, ["kaos"])

def get_bottom_options(activity, temperature, gender):
    """Get bottom outfit options"""
    options = {
        "kondangan": {
            "perempuan": ["rok", "celana bahan"],
            "laki-laki": ["celana bahan", "celana formal"]
        },
        "bekerja": {
            "perempuan": ["celana bahan", "rok"],
            "laki-laki": ["celana bahan", "chino"]
        },
        "olahraga": {
            "perempuan": ["legging", "celana olahraga"],
            "laki-laki": ["celana olahraga", "celana pendek"]
        },
        "santai": {
            "perempuan": ["jeans", "celana panjang"],
            "laki-laki": ["jeans", "celana pendek" if temperature > 30 else "celana panjang"]
        },
        "berjalan": {
            "perempuan": ["jeans", "celana panjang"],
            "laki-laki": ["jeans", "celana panjang"]
        }
    }
    
    gender_key = normalize_gender(gender)
    return options.get(activity, options["santai"]).get(gender_key, ["celana panjang"])

def get_outerwear_options(weather_category, temperature):
    """Get outerwear options berdasarkan cuaca"""
    if weather_category in ["hujan"]:
        return ["jaket waterproof", "raincoat"]
    elif weather_category == "gerimis":
        return ["jaket ringan", "hoodie"]
    elif temperature < 25:
        return ["hoodie", "cardigan", "sweater"]
    elif weather_category == "mendung":
        return ["cardigan", "jaket tipis"]
    else:
        return ["none"]

def get_footwear_options(weather_category, activity, gender):
    """Get footwear options"""
    if weather_category in ["hujan", "gerimis"]:
        return ["boots", "sepatu waterproof"]
    
    if activity == "kondangan":
        if normalize_gender(gender) == "perempuan":
            return ["heels", "wedges", "flat shoes"]
        else:
            return ["pantofel", "loafers"]
    
    if activity == "olahraga":
        return ["sneakers", "running shoes"]
    
    if activity == "santai":
        return ["sandal", "sneakers"]
    
    return ["sneakers", "casual shoes"]
