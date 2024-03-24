from django.shortcuts import render
import json  
from django.shortcuts import render  
import urllib.request  
import json  
import datetime

# Create your views here.
def home(request):
    context = {}

    if request.method == 'POST':
        city = request.POST.get('city', '')
        if city:
            try:
                api_key = 'f70634dce363e835b5300ebe8ae51840'  # Replace this with your actual API key
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={api_key}'
                response = urllib.request.urlopen(url)
                data = json.loads(response.read())
                temperature_fahrenheit = data['main']['temp']
                temperature_celsius = (temperature_fahrenheit - 32) * 5/9 
                timestamp = data['dt']
                utc_time = datetime.datetime.utcfromtimestamp(data['dt'])
                date = utc_time.strftime('%Y-%m-%d')
                time_utc = utc_time.strftime('%H:%M:%S')
                time_12hr_format_utc = utc_time.strftime('%I:%M %p')

                sunrise_timestamp = data['sys']['sunrise']
                sunset_timestamp = data['sys']['sunset']

                sunrise_time = datetime.datetime.utcfromtimestamp(sunrise_timestamp)
                sunset_time = datetime.datetime.utcfromtimestamp(sunset_timestamp)

                formatted_sunrise_time = sunrise_time.strftime('%Y-%m-%d %H:%M:%S')
                formatted_sunset_time = sunset_time.strftime('%Y-%m-%d %H:%M:%S')
                
                context = {
                    'city': city,
                    'country_code': data['sys']['country'],
                    'coordinate': f"{data['coord']['lon']} {data['coord']['lat']}",
                    'temp': f"{temperature_celsius:.2f}°C",  # Display temperature in Celsius with 2 decimal places
                    'pressure': data['main']['pressure'],
                    'humidity': data['main']['humidity'],
                    'sea_level': data['main']['sea_level'],
                    'clouds': data['clouds']['all'],
                    'weather': data['weather'][0]['main'],
                    'wind_speed': data['wind']['speed'],
                    'date': date,
                    'time_12hr_format_utc': time_12hr_format_utc,
                    'sunrise_time': formatted_sunrise_time,
                    'sunset_time': formatted_sunset_time

                
                    
                }
            except Exception as e:
                context['error_message'] = f"Error: {e}"
        else:
            context['error_message'] = "Please enter a city name."

    return render(request, 'home.html', context)
