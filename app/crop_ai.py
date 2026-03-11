def recommend_crop(temp, humidity):

    if temp > 30 and humidity > 60:
        return "Rice 🌾"

    elif temp > 25 and humidity < 50:
        return "Wheat 🌾"

    elif temp > 28 and humidity < 60:
        return "Maize 🌽"

    else:
        return "Potato 🥔"