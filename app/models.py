from django.db import models
from django.contrib.auth.models import User

class BirthChart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    birth_time = models.TimeField()
    birth_location = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    timezone = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.birth_date}"

class VargaChart(models.Model):
    birth_chart = models.ForeignKey(BirthChart, on_delete=models.CASCADE)
    chart_type  = models.CharField(max_length=10)
    chart_data  = models.JSONField()
    svg_url     = models.URLField(blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
