from django.test import TestCase
from .utils import str_to_snake_case
from django.contrib.auth.models import Group
from .models import Family
from .services import FamilyService
from apps.users.services import register_user

class UsersUtilTestCase(TestCase):

    def test_that_strings_are_converted_to_snake_case(self):
        in_str = "Meine Fam1l1engruppe!1!"
        exp_str = "meine_fam1l1engruppe!1!"

        snake_case = str_to_snake_case(in_str)
        self.assertEquals(snake_case, exp_str)


class UsersServiceTestCase(TestCase):
    def setUp(self):
        self.users = [
            register_user(username='test1', password='pass123', email='test@te-st.com'),
            register_user(username='test2', password='pass123', email='test@te-st.com'),
        ]

        self.families = [
            FamilyService().create_family(self.users[0], 'My Family')
        ]

    """
    We want to remove all Meal objects created during the tests
    to make sure, that we can test `get_all_meals` etc.
    """
    def tearDown(self):
        all_families = Family.objects.all()
        for family in all_families:
            found = [ f for f in self.families if f['id'] == family.id ]
            if len(found) == 0:
                family.delete()

        return super().tearDown()
    
    def test_get_all_groups_of_user(self):
        groups = FamilyService().get_all_of_user(self.users[0])
        self.assertEqual(len(groups), 2)

    def test_creation_of_new_groups(self):
        user = self.users[0]
        group_name = 'New Group!'

        dict = FamilyService().create_family(user, group_name)

        group = Group.objects.filter(name=dict['name']).first()
        self.assertIsNotNone(group)
        self.assertEqual(group.name, str_to_snake_case(group_name))

        family = Family.objects.filter(id=group.id).first()
        self.assertIsNotNone(family)
        self.assertFalse(family.personal)
        self.assertEqual(family.family_name, group_name)

    def test_deletion_of_group(self):
        user = self.users[0]
        group_name = 'New Group!'

        service = FamilyService()
        dict = service.create_family(user, group_name)

        service.delete_group(user, dict['id'])

        self.assertFalse(Group.objects.filter(id=dict['id']).exists())
        self.assertFalse(Family.objects.filter(id=dict['id']).exists())

    def test_that_deletion_of_group_fails_for_non_owner(self):
        user = self.users[0]
        group_name = 'New Group!'

        service = FamilyService()
        dict = service.create_family(user, group_name)

        self.assertRaises(Exception, service.delete_group, self.users[1], dict['id'])

    def test_removal_from_group(self):
        user = self.users[0]
        user_to_remove = self.users[1]
        family = self.families[0]

        service = FamilyService()
        service.add_user(user, family['id'], user_to_remove.username)

        service.remove_user(user, family['id'], user_to_remove.username)

        self.assertIsNone(user_to_remove.groups.filter(id=family['id']).first())

    def test_that_removal_from_nonexisting_groups_fails(self):
        user = self.users[0]
        self.assertRaises(Exception, FamilyService().remove_user, user, 'this_doesnt_exist', user)

    def test_that_removal_from_groups_without_membership_fails(self):
        # as user[1] is not part of families[0], this should fail
        self.assertRaises(Exception, FamilyService().remove_user, self.users[1], self.families[0].id, self.users[0].username)

    def test_that_removal_of_users_without_membership_from_groups_fails(self):
        self.assertRaises(Exception, FamilyService().remove_user, self.users[0], self.families[0].id, self.users[1].username)


