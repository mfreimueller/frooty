import logging
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from .models import Family, FamilySerialize
from .utils import str_to_snake_case

class FamilyService:

    def create_family(self, user: User, family_name: str, personal = False):
        internal_group_name = str_to_snake_case(family_name)

        family_group = Family.objects.create(name=internal_group_name, family_name=family_name, personal=personal)
        family_group.save()

        user.groups.add(family_group)
        user.save()

        return FamilySerialize(family_group).data

    def add_user(self, user: User, family_id: int, user_name: str):
        group = user.groups.get(id=family_id)
        if group is None:
            raise Exception(f"User is not part of family with id {family_id}.")
        
        family = Family.objects.filter(id=family_id).first()
        if family is None:
            raise Exception(f"There is no family with the id {family_id}.")
        
        if family.personal:
            raise Exception(f"Not allowed to interact with personal group.")

        user_to_add = User.objects.filter(username=user_name).first()
        if user_to_add is None:
            raise Exception(f"No user named {user_name} found.")
        
        user_to_add.groups.add(family)
        user_to_add.save()

    def remove_user(self, user: User, family_id: int, user_name: str):
        group = user.groups.get(id=family_id)
        if group is None:
            raise Exception(f"User is not part of a family with id {family_id}.")
        
        family = Family.objects.get(id=family_id)
        if family is None:
            raise Exception(f"There is no family with id {family_id}.")
        
        if family.personal:
            raise Exception(f"Not allowed to interact with personal group.")
        
        user_to_remove = User.objects.filter(username=user_name).first()
        if user_to_remove is None:
            raise Exception(f"No user named {user_name} found.")
        
        if not user_to_remove.groups.filter(id=family_id).exists():
            raise Exception(f"User named {user_name} is not a member of group {family_id}.")
        
        user_to_remove.groups.remove(family)
        user_to_remove.save()

        # delete the group if it becomes empty
        if not family.user_set.exists():
            family.delete()
            group.delete() # necessary?

    def delete_group(self, user: User, family_name: str):
        pass # TODO
    
    def update_group(self, user: User, family_id: int, new_family_name: str):
        pass

    def get_all_of_user(self, user: User):
        families = []

        for group in user.groups.all():
            family = Family.objects.get(id=group.id)
            families.append(family)

        return FamilySerialize(families, many=True).data
