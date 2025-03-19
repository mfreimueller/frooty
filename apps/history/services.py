from .models import History, HistorySerialize
from django.db import transaction
import logging

def get_all_history():
    all_meals = History.objects.all()
    return HistorySerialize(all_meals, many=True).data

@transaction.atomic
def add_history(meals):
    logger = logging.getLogger(__name__)

    created_history_items = []

    for meal in meals:
        logger.debug(f"Adding history {meal}...")
        history_object = History.objects.create(meal=meal)
        history_object.save()

        created_history_items.append(history_object)
    
    return HistorySerialize(created_history_items, many=True).data

def delete_history_item(history_id):
    logger = logging.getLogger(__name__)

    logger.debug(f"Deleting history item with id {history_id}...")#

    try:
        history_object = History.objects.get(id=history_id)
    except Exception as e:
        logger.error(f"No history item with id {history_id} found!")
        raise Exception(f"No history item with id {history_id} found!")
    
    history_object.delete()


def update_history_item(history_id, meal):
    logger = logging.getLogger(__name__)

    logger.debug(f"Updating history item with id {history_id}...")

    try:
        history_object = History.objects.get(id=history_id)
    except Exception as e:
        logger.error(f"No history item with id {history_id} found!")
        raise Exception(f"No history item with id {history_id} found!")
    
    history_object.meal = meal
    history_object.save()