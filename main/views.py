from django.shortcuts import render
from django.contrib import messages
from .forms import SearchForm
from .services import get_forecast_data, get_current_weather
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
            data = get_forecast_data(city)
            current_weather = get_current_weather(city)
            if data == 404:
                messages.add_message(request, messages.INFO, f'City "{city} not found!"')
                return redirect('index')
            
            form = SearchForm()
            context = {
                'form': form,
                'data': data,
                'current': current_weather
            }
            return render(request, 'main/index.html', context)
    else:
        form = SearchForm()
    return render(request, 'main/index.html', {'form': form})
