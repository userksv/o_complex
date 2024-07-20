from django.test import SimpleTestCase
from django.urls import reverse, resolve

from main.views import index, history, city_statistics


class TestUrls(SimpleTestCase):
    '''Testing urls paths to the corresponding view functions'''
    def test_index_url(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)
    
    def test_history_url(self):
        url = reverse('history', kwargs={'city': 'Moscow'})
        self.assertEqual(resolve(url).func, history)
    
    def test_city_statistics_url(self):
        url = reverse('statistics')
        self.assertEqual(resolve(url).func, city_statistics)
