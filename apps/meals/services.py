from .models import Meal, MealSerialize
from django.db import IntegrityError, transaction
import logging

def get_all_meals():
    all_meals = Meal.objects.all()
    return MealSerialize(all_meals, many=True).data

@transaction.atomic
def add_meal(meal):
    logger = logging.getLogger(__name__)

    logger.debug(f"Adding meal {meal['name']}...")

    try:
        meal_object = Meal.objects.create(**meal)
        meal_object.save()
    except IntegrityError as e:
        logger.error(f"Failed to create meal with name '{meal['name']}': Meal already exists!")
        raise Exception(f"Failed to create meal with name '{meal['name']}': Meal already exists!")

    return MealSerialize(meal_object).data

def delete_meal(meal_id):
    logger = logging.getLogger(__name__)

    logger.debug(f"Deleting meal with id {meal_id}...")#

    try:
        meal_object = Meal.objects.get(id=meal_id)
    except Exception as e:
        logger.error(f"No meal with id {meal_id} found!")
        raise Exception(f"No meal with id {meal_id} found!")
    
    meal_object.delete()


def update_meal(meal_id, meal):
    logger = logging.getLogger(__name__)

    logger.debug(f"Updating meal with id {meal_id}...")

    try:
        meal_object = Meal.objects.get(id=meal_id)
    except Exception as e:
        logger.error(f"No meal with id {meal_id} found!")
        raise Exception(f"No meal with id {meal_id} found!")
    
    meal_object.update(**meal)