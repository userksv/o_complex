import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()
API_KEY = os.getenv('API_KEY')

def get_forecast_data(city: str):
    units = 'metric'
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&units={units}&appid={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        data = deserialize_forecast(response.json())
        return data
    except requests.exceptions.HTTPError as e:
        return e.response.status_code

def get_current_weather(city: str):
    units = 'metric'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as e:
        return e.response.status_code


def deserialize_forecast(data: dict):
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

import pprint

pprint.pprint(get_current_weather('Seoul'))