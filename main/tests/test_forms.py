# tests/test_forms.py
from django.test import TestCase
from main.forms import SearchForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit


class SearchFormTest(TestCase):
    def test_form_valid_data(self):
        form_data = {'city_name': 'Novosibirsk'}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form_data = {'city_name': ''}
        form = SearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['city_name'], ['This field is required.'])

    def test_form_placeholder(self):
        form = SearchForm()
        self.assertIn('placeholder', form.fields['city_name'].widget.attrs)
        self.assertEqual(form.fields['city_name'].widget.attrs['placeholder'], 'e.g. Novosibirsk')

    def test_form_widget_class(self):
        form = SearchForm()
        self.assertIn('class', form.fields['city_name'].widget.attrs)
        self.assertEqual(form.fields['city_name'].widget.attrs['class'], 'form-control')

    def test_form_datalist(self):
        form = SearchForm()
        self.assertIn('list', form.fields['city_name'].widget.attrs)
        self.assertEqual(form.fields['city_name'].widget.attrs['list'], 'cities')

    def test_form_helper(self):
        form = SearchForm()
        self.assertEqual(form.helper.form_method, 'post')
        self.assertIn('city_name', form.helper.layout.fields[0].fields)
        self.assertEqual(form.helper.layout.fields[0].fields[0], 'city_name')
        self.assertIsInstance(form.helper.layout.fields[1].fields[0], Submit)
        self.assertEqual(form.helper.layout.fields[1].fields[0].name, 'submit')
        self.assertEqual(form.helper.layout.fields[1].fields[0].value, 'Search')
        self.assertEqual(form.helper.layout.fields[1].fields[0].field_classes, 'btn btn-primary btn btn-primary mb-2')
