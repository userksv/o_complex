import os
import requests


def request_by_city(city: str):
    
    API_KEY = os.getenv('API_KEY')
    unit = 'metric'
    # url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}' # by coordinates
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units={unit}&appid={API_KEY}' # by city name
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        return e.response.status_code
    