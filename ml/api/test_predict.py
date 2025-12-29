from predict import predict_outfit

input_data = {
    "gender": "male",
    "season": "summer",
    "activity": "casual",
    "temperature": 32,
    "humidity": 70,
}

outfits, images = predict_outfit(input_data)

print("Outfits:", outfits)
print("Images:", images)
