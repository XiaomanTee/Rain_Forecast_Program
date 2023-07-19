import datetime
import requests
import geocoder
import os

def date():
    today = datetime.date.today()
    input_date = input("Enter a date(YYYY-MM-DD) or press 'enter' for tomorrow: ")

    if input_date == "":
        searched_date = today + datetime.timedelta(days=1)
    else:
        try:
            searched_date = datetime.datetime.strptime(input_date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format")
            exit()
        
    return searched_date.strftime("%Y-%m-%d")

def location(city):
    g = geocoder.osm(city)
    
    return g.latlng

def weather(latitude, longitude, searched_date):
    endpoint_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}"
    response = requests.get(endpoint_url)

    if response.status_code == 200:
        weather_data = response.json()
        precipitation = weather_data["daily"]["precipitation_sum"][0]

        return precipitation
    else:
        return None

def result(prediction):
    if prediction > 0.0:
        return "It will rain"
    elif prediction == 0.0:
        return "It will not rain"
    else:
        return "I don't know"

def save_result(city, searched_date, precipitation):
    forecast_result = result(precipitation)
    with open("weather.txt", "a") as fd:
        fd.write(f"{city}: precipitation value is {precipitation} on {searched_date} ({forecast_result})\n")

def read_result(city, date):
    with open("weather.txt") as fd:
        for lines in fd:
            line = lines.split()
            searched_city = line[0].split(":")[0]
            searched_date = line[6]

            if searched_city == city and searched_date == date:
                return lines

def main():
    file = os.path.exists("weather.txt")
    searched_date = date()
    city = input("Enter a city: ").lower()
    
    if city == "":
        print("Please enter a city!")
        exit()

    latitude, longitude = location(city)

    if latitude is None or longitude is None:
        print("Invalid city")
        exit()

    if file:
        prediction_result = read_result(city, searched_date)

        if prediction_result == None:
            prediction = weather(latitude, longitude, searched_date)
            prediction = float(prediction)
            prediction_result = result(prediction)

            print("*****************************************")
            print(f"City: {city}        Date: {searched_date}")
            print(f"{prediction_result}")
            print(f"The precipitation value: {prediction}")
            print("*****************************************")

            save_result(city, searched_date, prediction)
        else:
            print(prediction_result)
    else:
        prediction = weather(latitude, longitude, searched_date)
        prediction = float(prediction)
        prediction_result = result(prediction)

        print("*****************************************")
        print(f"City: {city}        Date: {searched_date}")
        print(f"{prediction_result}")
        print(f"The precipitation value: {prediction}")
        print("*****************************************")

        save_result(city, searched_date, prediction)

if __name__ == "__main__":
    main()
