from django.test import TestCase
from django.contrib.auth.models import Group, User
from apps.families.models import Family
from .services import register_user

class UsersServiceTestCase(TestCase):
    def setUp(self):
        self.users = [
            User.objects.create(username='test', password='pass123', email='test@te-st.com')
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
