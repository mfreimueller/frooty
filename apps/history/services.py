from .models import History, HistorySerialize
from django.db import transaction
import logging
from django.contrib.auth.models import User
from apps.families.services import FamilyService

class HistoryService:

    def get_all_of_family(self, user: User, family_id: int):
        logger = logging.getLogger(__name__)

        if not FamilyService().is_user_part_of_family(user, family_id):
            logger.error(f'User {user.id} attempted to access family {family_id}!')
            raise Exception(f'User is not part of family {family_id}')

        history_of_family = History.objects.filter(family_id=family_id).all()
        return HistorySerialize(history_of_family, many=True).data

    @transaction.atomic
    def add_history(self, user: User, meals: list[str], family_id: int):
        logger = logging.getLogger(__name__)

        if not FamilyService().is_user_part_of_family(user, family_id):
            logger.error(f'User {user.id} attempted to access family {family_id}!')
            raise Exception(f'User is not part of family {family_id}')

        created_history_items = []

        for meal in meals:
            logger.debug(f"Adding history {meal}...")
            history_object = History.objects.create(meal=meal, family_id=family_id)
            history_object.save()

            created_history_items.append(history_object)
    
        return HistorySerialize(created_history_items, many=True).data

    def delete_history_item(self, user: User, history_id: int):
        logger = logging.getLogger(__name__)

        logger.debug(f"Deleting history item with id {history_id}...")#

        history_object = self._get_history_object(history_id, user)
        history_object.delete()

    def update_history_item(self, user: User, history_id: int, meal: str):
        logger = logging.getLogger(__name__)

        logger.debug(f"Updating history item with id {history_id}...")

        history_object = self._get_history_object(history_id, user)
        
        history_object.meal = meal
        history_object.save()

    # retrieve history object and perform permission check.
    def _get_history_object(self, history_id: int, user: User):
        logger = logging.getLogger(__name__)

        try:
            history_object = History.objects.get(id=history_id)
        except Exception as e:
            logger.error(f"No history item with id {history_id} found!")
            raise Exception(f"No history item with id {history_id} found!")
        
        if not history_object.family.is_user_part(user):
            logger.error(f'User {user.id} attempted to access family {history_object.family.id}!')
            raise Exception(f'User is not part of family {history_object.family.id}')
        
        return history_object
        