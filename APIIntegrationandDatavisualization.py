import requests
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set style
sns.set(style="whitegrid")

# Your OpenWeatherMap API Key (replace with your own)
API_KEY = "your_api_key_here"
CITY = "London"
URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

def fetch_weather_data():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch data: " + response.text)

def parse_weather_data(data):
    forecasts = data["list"]
    parsed_data = {
        "datetime": [],
        "temperature": [],
        "humidity": [],
        "weather_main": []
    }

    for entry in forecasts:
        dt = datetime.fromtimestamp(entry["dt"])
        temp = entry["main"]["temp"]
        humidity = entry["main"]["humidity"]
        weather_main = entry["weather"][0]["main"]

        parsed_data["datetime"].append(dt)
        parsed_data["temperature"].append(temp)
        parsed_data["humidity"].append(humidity)
        parsed_data["weather_main"].append(weather_main)

    return parsed_data

def visualize_data(data):
    plt.figure(figsize=(14, 10))

    # Plot 1: Temperature Trend
    plt.subplot(3, 1, 1)
    sns.lineplot(x=data["datetime"], y=data["temperature"], marker="o", color="tab:orange")
    plt.title("Temperature Trend (°C)")
    plt.xlabel("Date & Time")
    plt.ylabel("Temperature")
    plt.xticks(rotation=45)

    # Plot 2: Humidity
    plt.subplot(3, 1, 2)
    sns.barplot(x=data["datetime"], y=data["humidity"], color="skyblue")
    plt.title("Humidity Levels (%)")
    plt.xlabel("Date & Time")
    plt.ylabel("Humidity")
    plt.xticks(rotation=45)

    # Plot 3: Weather Condition Frequency
    plt.subplot(3, 1, 3)
    sns.countplot(x=data["weather_main"], palette="Set2")
    plt.title("Weather Condition Frequency")
    plt.xlabel("Condition")
    plt.ylabel("Count")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    try:
        raw_data = fetch_weather_data()
        weather_data = parse_weather_data(raw_data)
        visualize_data(weather_data)
    except Exception as e:
        print("Error:", e)
