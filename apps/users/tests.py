from django.test import TestCase
from .utils import str_to_snake_case
from django.contrib.auth.models import Group, User
from .models import Family
from .services import register_user, create_new_group, remove_user_from_group

class UsersUtilTestCase(TestCase):

    def test_that_strings_are_converted_to_snake_case(self):
        in_str = "Meine Fam1l1engruppe!1!"
        exp_str = "meine_fam1l1engruppe!1!"

        snake_case = str_to_snake_case(in_str)
        self.assertEquals(snake_case, exp_str)


class UsersServiceTestCase(TestCase):
    def setUp(self):
        self.users = [
            User.objects.create(username='test', password='pass123', email='test@te-st.com')
        ]

        family = Family.objects.create(name='my_family', family_name='My Family')
        self.users[0].groups.add(family)
        self.families = [
            family
        ]

    """
    We want to remove all Meal objects created during the tests
    to make sure, that we can test `get_all_meals` etc.
    """
    def tearDown(self):
        all_users = User.objects.all()
        for user in all_users:
            found = [ u for u in self.users if u.id == user.id ]
            if len(found) == 0:
                user.delete()
        
        all_families = Family.objects.all()
        for family in all_families:
            found = [ f for f in self.families if f.id == family.id ]
            if len(found) == 0:
                family.delete()

        return super().tearDown()

    def test_that_new_user_exists(self):
        username = 'uname'
        password = 'passsss'
        email = 'a1234@fg4.com'

        register_user(username, email, password)
        new_user = User.objects.filter(username=username).first

        self.assertIsNotNone(new_user)

    def test_that_personal_group_of_new_user_exists(self):
        username = 'uname'
        password = 'passsss'
        email = 'a1234@fg4.com'

        register_user(username, email, password)
        new_user = User.objects.filter(username=username).first()
        group = new_user.groups.first()
        family = Family.objects.filter(id=group.id).first()

        self.assertIsNotNone(family)
        self.assertTrue(family.personal)

    def test_that_duplicated_usernames_arent_allowed(self):
        username = self.users[0].username
        password = 'passsss'
        email = 'a1234@fg4.com'

        self.assertRaises(Exception, register_user, username, email, password)

    def test_creation_of_new_groups(self):
        user = self.users[0]
        group_name = 'New Group!'

        dict = create_new_group(user, group_name)

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

        dict = create_new_group(user, group_name)

        remove_user_from_group(user, dict['name'], user)

        self.assertFalse(Group.objects.filter(name=dict['name']).exists())
        self.assertFalse(Family.objects.filter(family_name=dict['family_name']).exists())

    def test_that_removal_from_nonexisting_groups_fails(self):
        user = self.users[0]
        self.assertRaises(Exception, remove_user_from_group, user, 'this_doesnt_exist', user)

    def test_that_removal_from_groups_without_membership_fails(self):
        username = 'uname'
        password = 'passsss'
        email = 'a1234@fg4.com'

        register_user(username, email, password)
        new_user = User.objects.filter(username=username).first()

        self.assertRaises(Exception, remove_user_from_group, new_user, self.families[0].name, self.users[0].username)

    def test_that_removal_of_users_without_membership_from_groups_fails(self):
        username = 'uname'
        password = 'passsss'
        email = 'a1234@fg4.com'

        register_user(username, email, password)

        self.assertRaises(Exception, remove_user_from_group, self.users[0], self.families[0].name, username)
