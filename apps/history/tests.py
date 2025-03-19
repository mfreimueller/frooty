from django.test import TestCase
from .models import History
from .services import add_history, delete_history_item, get_all_history, update_history_item

# TODO: Add test cases for duplicated names.

class HistoryServiceTestCase(TestCase):
    def setUp(self):
        self.history = [
            History.objects.create(meal="Brotjause"),
            History.objects.create(meal="Sushi"),
            History.objects.create(meal="Leberkässemmel"),
            History.objects.create(meal="Fisch")
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
        meals = add_history([ "Toast", "Eierspeise" ])
        self.assertEqual(len(meals), 2)
        self.assertEqual(meals[0]['meal'], "Toast")
        self.assertEqual(meals[1]['meal'], "Eierspeise")

    def test_get_all_history(self):
        history_items = get_all_history()
        self.assertEqual(len(history_items), len(self.history))

    """
    This test makes sure that an existing history item is
    properly deleted.
    """
    def test_delete_existing_history_item(self):
        # we don't test add_history here, we assume that it's working,
        # as we already covered this above
        meal = add_history([ "Toast" ])
        history_id = meal[0]['id']

        try:
            delete_history_item(history_id)
        except Exception as e:
            self.fail(f"delete_history_item() raised an exception: {e}")

        self.assertIsNone(History.objects.filter(id=history_id).first())

    """
    This test makes sure that attempting to delete a
    non existing history item raises an exception and thusly fails.
    """
    def test_delete_missing_history_item(self):
        history_id = -999
        self.assertRaises(Exception, delete_history_item, history_id)

    """
    This test makes sure that updating existing history item works 
    and properly updates the item associated with an id.
    """
    def test_update_existing_history_item(self):
        # we don't test add_meals here, we assume that it's working,
        # as we already covered this above
        item = add_history([ "Toast" ])

        history_id = item[0]['id']
        
        try:
            update_history_item(history_id, 'Veganer Burger')
        except Exception as e:
            self.fail(f"update_meal() raised an exception: {e}")

        self.assertEqual(History.objects.filter(id=history_id).first().meal, 'Veganer Burger')

    """
    This test makes sure that attempting to update a non existing history item
    fails with an exception.
    """
    def test_update_missing_history_item(self):
        history_id = -999
        self.assertRaises(Exception, update_history_item, history_id, 'Veganer Burger')
