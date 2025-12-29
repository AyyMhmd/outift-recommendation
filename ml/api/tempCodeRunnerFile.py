from predict import predict_outfit

input_data = {
    "temperature": 28,
    "is_rainy": 0,
    "is_hot": 1,
    "is_cold": 0,
    "season_summer": 1,
    "season_rainy": 0,
    "season_winter": 0,
    "activity_casual": 1,
    "activity_formal": 0,
    "activity_sport": 0,
}

result = predict_outfit(input_data)
print("Rekomendasi outfit:", result)
