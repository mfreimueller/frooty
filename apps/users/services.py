import logging
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from apps.families.services import FamilyService

@transaction.atomic
def register_user(username, email, password):
    logger = logging.getLogger(__name__)
    logger.debug(f'Creating new user with name {username}')

    try:
        user = User.objects.create_user(username, email, password)
        logger.debug(f'Successfully created new user with name {username}')

        user_group_name = f'{user.username}_group'
        FamilyService().create_group(user, user_group_name, True)
    except Exception as e:
        logger.exception(e)
        raise e

def authenticate_user(request, username, password):
    logger = logging.getLogger(__name__)
    logger.debug(f'Attempting to authenticate user with name {username}')

    user = authenticate(request, username=username, passowrd=password)
    if user is not None:
        login(request, user)
        return True
    else:
        return False
    
def logout_user(request):
    logout(request)

def update_user_password(user: User, new_password: str):
    logger = logging.getLogger(__name__)
    logger.debug(f'Updating password of user with name {user.username}')

    user.set_password(new_password)
    user.save()
