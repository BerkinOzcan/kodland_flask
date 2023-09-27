# importing modules
import requests, json,time


# API base URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

# City Name
CITY = "Ankara"

# Your API key
API_KEY = "YOUR_API_KEY"

# updating the URL
URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY

URL_MY = "http://api.weatherapi.com/v1/forecast.json?key=e5f57591945a43e88ed104908232609&q=" + CITY + "&days=3&aqi=no&alerts=no"
response = requests.get(URL_MY)

def ep_to_day(ep):
    day = time.strftime('%A', time.localtime(ep))
    return day


if response.status_code == 200:
    
   # retrieving data in the json format
   data = response.json()
   print(f"{CITY:-^35}")
   # take the main dict block
   forecast = data['forecast']
   forecastdays = forecast['forecastday']
   for fc in range (len(forecastdays)):
      fc_epoch = forecastdays[fc]['date_epoch']
      fc_date = forecastdays[fc]['date']
      fc_day = forecastdays[fc]['day']
      mintemp_c = fc_day['mintemp_c']
      maxtemp_c = fc_day['maxtemp_c']
      dateinfo = "epoch date: " + str(fc_epoch) + ", " + "Full Date: " + fc_date + "-"+ ep_to_day(fc_epoch)
      tempinfo = "minimum temperature: " + str(mintemp_c) + "\nmaximum temperature: " + str(maxtemp_c)
      print(dateinfo)
      print(tempinfo)
      print("-------------------------------------")
      #print(ep_to_day(fc_epoch))
   
   #print(forecastday0date)
#    # getting temperature
#    temperature = main['temp']
#    # getting feel like
#    temp_feel_like = main['feels_like']  
#    # getting the humidity
#    humidity = main['humidity']
#    # getting the pressure
#    pressure = main['pressure']
   
   # weather report
#    weather_report = data['weather']
#    # wind report
#    wind_report = data['wind']
   
   
   
#    print(f"City ID: {data['id']}")   
#    print(f"Temperature: {temperature}")
#    print(f"Feel Like: {temp_feel_like}")    
#    print(f"Humidity: {humidity}")
#    print(f"Pressure: {pressure}")
#    print(f"Weather Report: {weather_report[0]['description']}")
#    print(f"Wind Speed: {wind_report['speed']}")
#    print(f"Time Zone: {data['timezone']}")

else:
   # showing the error message
   print("Error in the HTTP request")