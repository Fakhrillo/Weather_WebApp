from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

import openpyxl
# Create your views here.

workbook = openpyxl.load_workbook('weather_app/cities_list.xlsx')
worksheet = workbook['cities_list']


def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=b090d337828b8991f8ddf722ea7c7424'
    error_message = 0
    success_message = 0
    for row in worksheet.iter_rows(min_row=2):  # Start from the second row assuming headers are in the first row
        column1_value = row[0].value  # Access the first column value of each row
        column2_value = row[3].value  # Access the second column value of each row
        # Compare the values with your existing data
        cities_check = City.objects.all()
        city_names = tuple(city.name for city in cities_check)
        if request.method == 'POST':
            form_data = request.POST
            if column1_value == form_data['name'] or column2_value == form_data['name']:
                if form_data['name'] not in city_names:
                    form = CityForm(request.POST)
                    form.save()
                    success_message = 1
                else:
                    error_message = 1
        else:
            pass
    form = CityForm()

    cities = City.objects.all()

    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()
    
        city_weather = {
            'city': city.name,
            'temperature': round(r['main']['temp'] - 273.15, 2),
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)
    
    context = {'weather_data': weather_data, 'form': form, 'error_message': error_message, 'success_message':success_message}
    
    return render(request, 'weather_app/base.html', context)