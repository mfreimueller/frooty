import logging
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from .models import Family, FamilySerialize
from .utils import str_to_snake_case

@transaction.atomic
def register_user(username, email, password):
    logger = logging.getLogger(__name__)
    logger.debug(f'Creating new user with name {username}')

    try:
        user = User.objects.create_user(username, email, password)
        logger.debug(f'Successfully created new user with name {username}')

        user_group_name = f'{user.username}_group'

        family_group = Family.objects.create(name=user_group_name, family_name=user_group_name, personal=True)
        family_group.save()

        user.groups.add(family_group)
        user.save()
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

def create_new_group(user: User, group_name: str):
    internal_group_name = str_to_snake_case(group_name)

    family_group = Family.objects.create(name=internal_group_name, family_name=group_name, personal=False)
    family_group.save()

    user.groups.add(family_group)
    user.save()

    return FamilySerialize(family_group).data

def add_user_to_group(user: User, group_name: str, user_name: str):
    group = user.groups.filter(name=group_name).first()
    if group is None:
        raise Exception(f"User is not part of a family named {group_name}.")
    
    family = Family.objects.filter(id=group.id).first()
    if family is None:
        raise Exception(f"There is no family with the name {group_name}.")
    
    if family.personal:
        raise Exception(f"Not allowed to interact with personal group.")

    user_to_add = User.objects.filter(username=user_name).first()
    if user_to_add is None:
        raise Exception(f"No user named {user_name} found.")
    
    user_to_add.groups.add(family)
    user_to_add.save()

def remove_user_from_group(user: User, group_name: str, user_name: str):
    group = user.groups.filter(name=group_name).first()
    if group is None:
        raise Exception(f"User is not part of a family named {group_name}.")
    
    family = Family.objects.filter(id=group.id).first()
    if family is None:
        raise Exception(f"There is no family with the name {group_name}.")
    
    if family.personal:
        raise Exception(f"Not allowed to interact with personal group.")
    
    user_to_remove = User.objects.filter(username=user_name).first()
    if user_to_remove is None:
        raise Exception(f"No user named {user_name} found.")
    
    if not user_to_remove.groups.filter(name=group_name).exists():
        raise Exception(f"User named {user_name} is not a member of group {group_name}.")
    
    user_to_remove.groups.remove(family)
    user_to_remove.save()

    # delete the group if it becomes empty
    if not family.user_set.exists():
        family.delete()
        group.delete() # necessary?
