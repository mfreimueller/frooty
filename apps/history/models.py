from django.db import models
from rest_framework import serializers

class History(models.Model):
    meal = models.CharField(max_length=200)

class HistorySerialize(serializers.Serializer):
    id = serializers.IntegerField()
    meal = serializers.CharField(max_length=200)
