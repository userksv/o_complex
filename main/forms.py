from django import forms


class SearchForm(forms.Form):
    city_name = forms.CharField(max_length=128, label='Enter city')
