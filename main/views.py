from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404


from .forms import SearchForm
from .services import get_forecast_data, get_current_weather
from .models import UserHistory, City

from datetime import datetime

def index(request):
    session_id = create_session(request)
    user_history = create_user_history(session_id)
    user_history = get_user_history(session_id)
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city_name']
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
    return render(request, 'main/index.html', {'form': form, 'u_history': user_history})

def history(request, city: str):
    current_weather = get_current_weather(city)
    data = get_forecast_data(city)
    context = {
        'data': data,
        'current': current_weather,
        }
    return render(request, 'main/history.html', context)

def city_statistics(request):
    data = serializers.serialize("json", City.get_data(), fields=["name", "count"])
    return HttpResponse(data, content_type="application/json")


def create_session(request):
    if not request.session.session_key:
        session_id = request.session.create()
    session_id = request.session.session_key
    return session_id


def create_user_history(session_id: str):
    s = Session.objects.get(pk=session_id)
    user, created = UserHistory.objects.get_or_create(session_id=s)
    return user.get_last_city()

def get_user_history(session_id: str):
    s = Session.objects.get(pk=session_id)
    user = UserHistory.objects.get(session_id=s)
    return user.get_last_city()

def update_user_history(session_id: str, city: str):
    s = Session.objects.get(pk=session_id)
    user = UserHistory.objects.get(session_id=s)
    user.update_last_city(city)
    user.save()