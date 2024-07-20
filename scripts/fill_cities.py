import csv
from main.models import City

def fill_out_db():
    with open('scripts/worldcities.csv', 'r')as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader, None)
        cities = [city[1] for city in reader]
        objs = [City(name=city) for city in set(cities)]
        City.objects.bulk_create(objs)