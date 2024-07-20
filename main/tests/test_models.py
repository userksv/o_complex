from django.test import TestCase, Client
from django.contrib.sessions.models import Session
from django.utils import timezone
from main.models import UserHistory, City
from unittest.mock import patch



class UserHistoryModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.session_key = self.client.session.session_key

        self.session = Session.objects.get(pk=self.session_key)
        self.user_history = UserHistory.objects.create(
            session_id=self.session,
            last_city="New York"
        )
        
    def test_string_representation(self):
        expected_str = f'{self.session.pk} - {self.user_history.last_visit}'
        self.assertEqual(str(self.user_history), expected_str)

    def test_get_last_visit(self):
        self.assertEqual(self.user_history.get_last_visit(), self.user_history.last_visit)

    def test_get_last_city(self):
        self.assertEqual(self.user_history.get_last_city(), "New York")

    def test_update_last_city(self):
        self.user_history.update_last_city("Los Angeles")
        self.user_history.save()
        self.assertEqual(self.user_history.get_last_city(), "Los Angeles")


class CityModelTest(TestCase):
    def setUp(self):
        # Create City instances
        self.city1 = City.objects.create(name="New York", count=5)
        self.city2 = City.objects.create(name="Los Angeles", count=0)
        
    def test_string_representation(self):
        self.assertEqual(str(self.city1), "New York - 5")
        self.assertEqual(str(self.city2), "Los Angeles - 0")

    def test_get_data_class_method(self):
        searched_cities = City.get_data()
        self.assertIn(self.city1, searched_cities)
        self.assertNotIn(self.city2, searched_cities)

    def test_ordering(self):
        cities = City.objects.all()
        self.assertEqual(cities[0], self.city2)  # Los Angeles should come before New York
        self.assertEqual(cities[1], self.city1)

