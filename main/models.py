from django.db import models
from django.contrib.sessions.models import Session


class UserHistory(models.Model):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    last_visit = models.DateTimeField(auto_now=True)
    last_city = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "User's History"

    def __str__(self) -> str:
        return f'{self.session_id.pk}'
    
    def get_last_visit(self):
        return self.last_visit

    def get_last_city(self):
        return self.last_city
    
    def update_last_city(self, city: str):
        self.last_city = city
        

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    count = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "City"

    def __str__(self) -> str:
        return self.name
    
    @classmethod
    def get_data(self):
        return City.objects.all()