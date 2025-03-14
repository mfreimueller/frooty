from apps.predictor.services import predict_meals
from .models import Meal, MealSerialize
from django.db import transaction
import logging

def plan_meals():
    predicted_meals = predict_meals()
    return predicted_meals

def get_all_meals():
    all_meals = Meal.objects.all()
    return MealSerialize(all_meals, many=True).data

@transaction.atomic
def add_meals(meals):
    logger = logging.getLogger(__name__)

    created_meals = []

    for meal in meals:
        logger.debug(f"Adding meal {meal}...")
        meal_object = Meal.objects.filter(meal=meal).first()

        if meal_object:
            logger.debug(f"Cloning meal {meal}.")
            meal_object.id = None
            meal_object.save()

            created_meals.append({
                'id': meal_object.pk,
                'meal': meal
            })
        else:
            logger.error(f"Meal with the name {meal} not found.")
            raise Exception(f"Meal with the name {meal} not found.")
    
    return created_meals
