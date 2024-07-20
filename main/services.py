from django.contrib.sessions.models import Session

import os, requests

from .models import City, UserHistory

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

def get_forecast_data(city: str):
    '''Request forecast data from API by city. Retrun custom serialized data'''
    units = 'metric'
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&units={units}&appid={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = serialize_forecast(response.json())
        track_city(city)
        return data
    except requests.exceptions.HTTPError as e:
        return e.response.status_code

def get_current_weather(city: str):
    '''Request current data by city. Return json data'''
    units = 'metric'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as e:
        return e.response.status_code

def serialize_forecast(data: dict):
    '''Serializing data from openweather API. return dictionary'''
    records = {}
    records['city'] = data['city']['name']
    records['list'] = []
    for record in data['list']:
        if datetime.fromtimestamp(record['dt']).hour == 0:
            records['list'].append({
                'date_time' : datetime.fromtimestamp(record['dt']),
                'temp' : record['main']['temp'],
                'temp_min' : record['main']['temp_min'],
                'temp_max' : record['main']['temp_min'],
                'description' : record['weather'][0]['description'],
                'icon' : record['weather'][0]['icon'],
                })
    return records

def track_city(city: str):
    '''Increments city count'''
    obj, created = City.objects.get_or_create(name=city)
    if created:
        obj.count = 1
    else:
        obj.count += 1
    obj.save()
    return obj

def create_session(request):
    '''Create session_key for each new user'''
    if not request.session.session_key:
        session_id = request.session.create()
    session_id = request.session.session_key
    return session_id

def create_user_history(session_id: str):
    '''Create history model for each new user'''
    s = Session.objects.get(pk=session_id)
    user, created = UserHistory.objects.get_or_create(session_id=s)
    return user.get_last_city()

def get_user_history(session_id: str):
    '''Get user's history by session_id'''
    s = Session.objects.get(pk=session_id)
    user = UserHistory.objects.get(session_id=s)
    return user.get_last_city()

def update_user_history(session_id: str, city: str):
    '''Update user's last searched city by session_id'''
    s = Session.objects.get(pk=session_id)
    user = UserHistory.objects.get(session_id=s)
    user.update_last_city(city)
    user.save()