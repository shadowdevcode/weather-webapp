from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


def index(request):
    cities = City.objects.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=Your_API_KEY'

    if request.method == 'POST':
        # add actual request data to form for processing
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    weather_data = []
    for city in cities:

        city_weather = requests.get(url.format(city)).json()

        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }
        # Add the data for the current city into our list
        weather_data.append(weather)
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/index.html', context)    # Returns index.html template
