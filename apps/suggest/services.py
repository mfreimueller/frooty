from apps.suggest_logic.services import predict_meals
from django.contrib.auth.models import User
from apps.families.services import FamilyService
import datetime

def plan_meals(user: User, family_id: int, start_date: datetime.date):
    if not FamilyService().is_user_part_of_family(user, family_id):
        raise Exception(f"User named {user.username} is not a member of group {family_id}.")

    predicted_meals = predict_meals(family_id)

    date = start_date

    return_list = list()
    for meal in predicted_meals:
        return_list.append({
            'meal': meal,
            'familyId': family_id,
            'date': date.strftime('%Y-%m-%d')
        })

        date = date + datetime.timedelta(days=1)

    return return_list
