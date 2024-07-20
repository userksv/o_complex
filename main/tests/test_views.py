from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

from main.models import City, UserHistory

from unittest.mock import patch



class TestViews(TestCase):

    def setUp(self) -> None:
        City.objects.create(name="Anapa", count=3)
        City.objects.create(name="Novosibirsk", count=5)
        City.objects.create(name="Paris", count=1)

        self.client = Client()
        self.index_url = reverse('index')
        self.history_url = reverse('history', kwargs={'city': 'Moscow'})
        self.statistics_url = reverse('statistics')

    def test_main_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')

    
    def test_main_history_GET(self):
        response = self.client.get(self.history_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/history.html')

    def test_main_statistics_GET(self):
        response = self.client.get(self.statistics_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = response.json()
        # Testing json structure in response
        for item in data:
            self.assertIn("model", item)
            self.assertIn("fields", item)
            self.assertIn("name", item["fields"])
            self.assertIn("count", item["fields"])
            self.assertIsInstance(item["fields"]["name"], str)
            self.assertIsInstance(item["fields"]["count"], int)
    

class IndexViewTest(TestCase):
    @patch('main.views.create_session')
    @patch('main.views.create_user_history')
    @patch('main.views.get_user_history')
    @patch('main.views.get_forecast_data')
    @patch('main.views.get_current_weather')
    @patch('main.views.update_user_history')
    def test_index_post(self, mock_update_user_history, mock_get_current_weather, mock_get_forecast_data, mock_get_user_history, mock_create_user_history, mock_create_session):
        
        # Mock return values
        mock_create_session.return_value = 'test_session_id'
        mock_create_user_history.return_value = []
        mock_get_user_history.return_value = []
        mock_get_forecast_data.return_value = {
            'city': 'New York',
            'list': [
                {
                    'date_time': '2023-07-20 00:00:00',
                    'temp': 22,
                    'temp_min': 15,
                    'temp_max': 25,
                    'description': 'Sunny',
                    'icon': '01d'
                }
            ]
        }
        mock_get_current_weather.return_value = {
            'weather': [{'description': 'Clear', 'icon': '01d'}],
            'main': {'temp': 20, 'temp_min': 15, 'temp_max': 25},
            'name': 'New York'
        }

        client = Client()
        response = client.post(reverse('index'), {'city_name': 'New York'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')
        # Check context data
        self.assertIn('form', response.context)
        self.assertIn('data', response.context)
        self.assertIn('current', response.context)
        self.assertEqual(response.context['data'], {
            'city': 'New York',
            'list': [
                {
                    'date_time': '2023-07-20 00:00:00',
                    'temp': 22,
                    'temp_min': 15,
                    'temp_max': 25,
                    'description': 'Sunny',
                    'icon': '01d'
                }
            ]
        })
        self.assertEqual(response.context['current'], {
            'weather': [{'description': 'Clear', 'icon': '01d'}],
            'main': {'temp': 20, 'temp_min': 15, 'temp_max': 25},
            'name': 'New York'
        })

        # Check that the user history is updated
        mock_update_user_history.assert_called_once_with('test_session_id', 'New York')

    @patch('main.views.create_session')
    @patch('main.views.create_user_history')
    @patch('main.views.get_user_history')
    @patch('main.views.get_forecast_data')
    @patch('main.views.get_current_weather')
    @patch('main.views.update_user_history')
    def test_index_post_city_not_found(self, mock_update_user_history, mock_get_current_weather, mock_get_forecast_data, mock_get_user_history, mock_create_user_history, mock_create_session):
        # Mock return values
        mock_create_session.return_value = 'test_session_id'
        mock_create_user_history.return_value = []
        mock_get_user_history.return_value = []
        mock_get_forecast_data.return_value = 404

        client = Client()
        response = client.post(reverse('index'), {'city_name': 'InvalidCity'})

        # Check if the response is a redirect to the index
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))