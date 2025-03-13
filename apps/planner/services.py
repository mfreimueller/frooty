from django.core import serializers
from apps.predictor.services import predict_meals
from .models import Meal, MealSerialize

def plan_meals():
    predicted_meals = predict_meals()
    return predicted_meals

def get_all_meals():
    all_meals = Meal.objects.all()
    return MealSerialize(all_meals, many=True).data