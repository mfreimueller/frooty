from django.db import models
from rest_framework import serializers
from apps.families.models import Family

class History(models.Model):
    meal = models.CharField(max_length=200)
    date = models.DateField()
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='histories')

class HistorySerialize(serializers.ModelSerializer):
    familyId = serializers.IntegerField(source='family_id')

    class Meta:
        model = History
        fields = ['id', 'meal', 'date', 'familyId']
