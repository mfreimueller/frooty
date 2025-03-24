from django.test import TestCase
from django.contrib.auth.models import User
from .models import History
from .services import HistoryService
from apps.families.models import Family

# TODO: Add test cases for duplicated names.

class HistoryServiceTestCase(TestCase):
    def setUp(self):
        self.users = [
            User.objects.create_user(username='user', email='email@email.com', password='123'),
            User.objects.create_user(username='user2', email='email@email.com', password='123')
        ]

        self.family = Family.objects.create(family_name="My Family", personal=False, owner=self.users[0])
        self.users[0].groups.add(self.family)
        self.users[0].save()

        self.history = [
            History.objects.create(meal="Brotjause", family=self.family),
            History.objects.create(meal="Sushi", family=self.family),
            History.objects.create(meal="Leberkässemmel", family=self.family),
            History.objects.create(meal="Fisch", family=self.family)
        ]

    """
    We want to remove all history objects created during the tests
    to make sure, that we can test `get_all_history` etc.
    """
    def tearDown(self):
        all_history = History.objects.all()
        for item in all_history:
            found = [ h for h in self.history if h.id == item.id ]
            if len(found) == 0:
                item.delete()

        return super().tearDown()

    def test_add_history_items(self):
        meals = HistoryService().add_history(self.users[0], [ "Toast", "Eierspeise" ], self.family.id)
        self.assertEqual(len(meals), 2)
        self.assertEqual(meals[0]['meal'], "Toast")
        self.assertEqual(meals[1]['meal'], "Eierspeise")

    def test_get_all_history(self):
        history_items = HistoryService().get_all_of_family(self.users[0], self.family.id)
        self.assertEqual(len(history_items), len(self.history))

    def test_get_all_for_unauthorized_user(self):
        self.assertRaises(Exception, HistoryService().get_all_of_family, self.users[1], self.family.id)

    """
    This test makes sure that an existing history item is
    properly deleted.
    """
    def test_delete_existing_history_item(self):
        # we don't test add_history here, we assume that it's working,
        # as we already covered this above
        meal = HistoryService().add_history(self.users[0], [ "Toast" ], self.family.id)
        history_id = meal[0]['id']

        HistoryService().delete_history_item(self.users[0], history_id)
        self.assertIsNone(History.objects.filter(id=history_id).first())

    def test_delete_existing_history_item_for_unauthorized_user(self):
        # we don't test add_history here, we assume that it's working,
        # as we already covered this above
        meal = HistoryService().add_history(self.users[0], [ "Toast" ], self.family.id)
        history_id = meal[0]['id']
        
        self.assertRaises(Exception, HistoryService().delete_history_item, self.users[1], history_id)

    """
    This test makes sure that attempting to delete a
    non existing history item raises an exception and thusly fails.
    """
    def test_delete_missing_history_item(self):
        history_id = -999
        self.assertRaises(Exception, HistoryService().delete_history_item, self.users[0], history_id)

    """
    This test makes sure that updating existing history item works 
    and properly updates the item associated with an id.
    """
    def test_update_existing_history_item(self):
        # we don't test add_meals here, we assume that it's working,
        # as we already covered this above
        item = HistoryService().add_history(self.users[0], [ "Toast" ], self.family.id)

        history_id = item[0]['id']
        
        HistoryService().update_history_item(self.users[0], history_id, 'Veganer Burger')
        self.assertEqual(History.objects.filter(id=history_id).first().meal, 'Veganer Burger')

    def test_update_existing_history_item_for_unauthorized_user(self):
        # we don't test add_meals here, we assume that it's working,
        # as we already covered this above
        item = HistoryService().add_history(self.users[0], [ "Toast" ], self.family.id)

        history_id = item[0]['id']

        self.assertRaises(Exception, HistoryService().update_history_item, self.users[1], history_id, 'Veganer Burger')

    """
    This test makes sure that attempting to update a non existing history item
    fails with an exception.
    """
    def test_update_missing_history_item(self):
        history_id = -999
        self.assertRaises(Exception, HistoryService().update_history_item, self.users[0], history_id, 'Veganer Burger')
