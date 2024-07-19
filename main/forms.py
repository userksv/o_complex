from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit

class SearchForm(forms.Form):
    city_name = forms.CharField(
        max_length=128, label='Enter city',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'e.g. New York',
                'class': 'form-control',
                'list': 'cities'
            }
        ))

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Field('city_name'),
            ButtonHolder(
                Submit('submit', 'Search', css_class='btn btn-primary mb-2')
            )
        )
