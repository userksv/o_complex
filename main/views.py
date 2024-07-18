from django.shortcuts import render
from django.contrib import messages
from .forms import SearchForm
from .services import request_by_city
from django.shortcuts import render, redirect
import datetime


# Create your views here.
def index(request):
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # get city name
            city = form.cleaned_data['city_name']
            data = request_by_city(city)
            if data == 404:
                messages.add_message(request, messages.INFO, f'City "{city} not found!"')
                return redirect('index')
            r = deserialize(data)
            form = SearchForm()
            context = {
                'form': form,
                'data': r
            }
            return render(request, 'main/index.html', context)
    else:
        form = SearchForm()
    return render(request, 'main/index.html', {'form': form})



def serialize_objects(objects):
    result = []
    for obj in objects:
        result.append(obj)
    return result

def deserialize(data):
    result = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'weather': data['weather'][0]['main'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon'],
        'date_time': datetime.datetime.fromtimestamp(data['dt']),
        'lon': data['coord']['lon'],
        'lat': data['coord']['lat'],
        }
    print(len(result))
    return result
