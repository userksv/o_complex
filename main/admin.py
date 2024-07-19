from django.contrib import admin
from .models import City, UserHistory
from django.contrib.sessions.models import Session


admin.site.register(City)
admin.site.register(UserHistory)
admin.site.register(Session)