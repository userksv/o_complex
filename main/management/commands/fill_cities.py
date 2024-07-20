from django.core.management.base import BaseCommand, CommandError
from main.models import City
from scripts.fill_cities import fill_out_db


class Command(BaseCommand):
    '''Command to populate City model from json file using script in scripts/fill_cities module'''
    def handle(self, *args, **options):
        fill_out_db()