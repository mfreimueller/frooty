from django.test import TestCase
from .models import Meal
from .services import add_meals, delete_meal, get_all_meals, update_meal

class MealServiceTestCase(TestCase):
    def setUp(self):
        self.meals = [
            Meal.objects.create(meal="Brotjause", complexity=1),
            Meal.objects.create(meal="Sushi", complexity=6),
            Meal.objects.create(meal="Leberkässemmel", complexity=2),
            Meal.objects.create(meal="Fisch", complexity=4)
        ]

    """
    We want to remove all Meal objects created during the tests
    to make sure, that we can test `get_all_meals` etc.
    """
    def tearDown(self):
        all_meals = Meal.objects.all()
        for meal in all_meals:
            found = [ m for m in self.meals if m.id == meal.id ]
            if len(found) == 0:
                meal.delete()

        return super().tearDown()

    def test_add_meals(self):
        meals = add_meals(["Brotjause", "Sushi"])
        self.assertEqual(len(meals), 2)
        self.assertEqual(meals[0]['meal'], "Brotjause")
        self.assertEqual(meals[1]['meal'], "Sushi")

    def test_get_all_meals(self):
        meals = get_all_meals()
        self.assertEqual(len(meals), len(self.meals))

    """
    This test makes sure that an existing meal is
    properly deleted.
    """
    def test_delete_existing_meal(self):
        # we don't test add_meals here, we assume that it's working,
        # as we already covered this above
        meals = add_meals([ "Brotjause" ])

        meal_id = meals[0]['id']

        try:
            delete_meal(meal_id)
        except Exception as e:
            self.fail(f"delete_meal() raised an exception: {e}")

        self.assertIsNone(Meal.objects.filter(id=meal_id).first())

    """
    This test makes sure that attempting to delete a
    non existing meal raises an exception and thusly fails.
    """
    def test_delete_missing_meal(self):
        meal_id = -999
        self.assertRaises(Exception, delete_meal, meal_id)

    """
    This test makes sure that updating existing meals works 
    and properly updates the meal associated with an id.
    """
    def test_update_existing_meal(self):
        # we don't test add_meals here, we assume that it's working,
        # as we already covered this above
        meals = add_meals([ "Brotjause" ])

        meal_id = meals[0]['id']
        
        try:
            update_meal(meal_id, 'Sushi')
        except Exception as e:
            self.fail(f"update_meal() raised an exception: {e}")

        self.assertEqual(Meal.objects.filter(id=meal_id).first().meal, 'Sushi')

    """
    This test makes sure that attempting to update a non existing meal
    fails with an exception.
    """
    def test_update_missing_meal(self):
        meal_id = -999
        self.assertRaises(Exception, update_meal, meal_id, 'Sushi')
