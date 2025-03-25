import logging
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from apps.families.services import FamilyService
from rest_framework.authtoken.models import Token

@transaction.atomic
def register_user(username, email, password):
    logger = logging.getLogger(__name__)
    logger.debug(f'Creating new user with name {username}')

    try:
        user = User.objects.create_user(username, email, password)
        logger.debug(f'Successfully created new user with name {username}')

        Token.objects.create(user=user)
        logger.debug(f'Successfully created unique token for new user with name {username}')

        user_group_name = f'{user.username}_group'
        FamilyService().create_family(user, user_group_name, True)
        logger.debug(f'Successfully added new user with name {username} to personal family {user_group_name}')
    except Exception as e:
        logger.exception(e)
        raise e
    
    return user

def update_user_password(user: User, new_password: str):
    logger = logging.getLogger(__name__)
    logger.debug(f'Updating password of user with name {user.username}')

    user.set_password(new_password)
    user.save()

    token = Token.objects.find(user=user)
    token.key = None
    token.save()

    logger.debug(f'Generated new token for user with name {user.username}')
