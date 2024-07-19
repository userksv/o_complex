from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers

from .models import City
from .forms import SearchForm
from .services import (
    get_forecast_data, get_current_weather, create_session, 
    create_user_history, get_user_history, update_user_history,)


def index(request):
    session_id = create_session(request)
    user_history = create_user_history(session_id)
    user_history = get_user_history(session_id)
    cities = City.objects.all() # for input autocomlete
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city_name'].lower().title()
            data = get_forecast_data(city)
            if data == 404:
                messages.add_message(request, messages.INFO, f'City "{city} not found!"')
                return redirect('index')
            
            current_weather = get_current_weather(city)
            update_user_history(session_id, city)
            form = SearchForm()
            context = {
                'form': form,
                'data': data,
                'current': current_weather,
            }
            return render(request, 'main/index.html', context)
    else:
        form = SearchForm()
        context = {
            'form': form,
            'u_history': user_history,
            'cities': cities
        }
    return render(request, 'main/index.html', context)


def history(request, city: str):
    '''Return context data by city'''
    current_weather = get_current_weather(city)
    data = get_forecast_data(city)
    context = {
        'data': data,
        'current': current_weather,
        }
    return render(request, 'main/history.html', context)


def city_statistics(request):
    '''Return city statistics as a json'''
    data = serializers.serialize("json", City.get_data(), fields=["name", "count"])
    return HttpResponse(data, content_type="application/json")