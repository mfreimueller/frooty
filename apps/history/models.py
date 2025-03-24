from django.db import models
from rest_framework import serializers
from apps.families.models import Family

class History(models.Model):
    meal = models.CharField(max_length=200)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='histories')

class HistorySerialize(serializers.Serializer):
    id = serializers.IntegerField()
    meal = serializers.CharField(max_length=200)
