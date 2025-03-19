from apps.suggest_logic.services import predict_meals
from .models import Meal, MealSerialize
from django.db import transaction
from .utils import copy_meal_to
import logging

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

def update_meal(meal_id, meal):
    logger = logging.getLogger(__name__)

    logger.debug(f"Updating meal with id {meal_id}...")

    # we retrieve the meal identified by `id`, which will be
    # updated with the contents found in the meal identified
    # by the name of `meal`.

    try:
        meal_destination_object = Meal.objects.get(id=meal_id)
    except Exception as e:
        logger.error(f"No meal with id {meal_id} found!")
        raise Exception(f"No meal with id {meal_id} found!")
    
    meal_source_object = Meal.objects.filter(meal=meal).first()
    if not meal_source_object:
        logger.error(f"No meal with name {meal} found!")
        raise Exception(f"No meal with name {meal} found!")

    meal_destination_object = copy_meal_to(meal_source_object, meal_destination_object)
    meal_destination_object.save()