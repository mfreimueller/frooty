from django.test import TestCase
from .models import Meal
from .services import add_meal, delete_meal, get_all_meals, update_meal

# TODO: Add test cases for duplicated names.

class MealServiceTestCase(TestCase):
    def setUp(self):
        self.meals = [
            Meal.objects.create(name="Brotjause", complexity=1),
            Meal.objects.create(name="Sushi", complexity=6),
            Meal.objects.create(name="Leberkässemmel", complexity=2),
            Meal.objects.create(name="Fisch", complexity=4)
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

    def test_add_meal(self):
        meal = add_meal({ "name": "Toast", "complexity": 2 })
        self.assertEqual(meal['name'], "Toast")

    def test_add_duplicated_meal(self):
        self.assertRaises(Exception, add_meal, { "name": "Brotjause", "complexity": 2 })

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
        meal = add_meal({ "name": "Toast", "complexity": 2 })

        meal_id = meal['id']

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
        meal = add_meal({ "name": "Toast", "complexity": 2 })

        meal_id = meal['id']
        
        try:
            update_meal(meal_id, { 'name': 'Veganer Burger' })
        except Exception as e:
            self.fail(f"update_meal() raised an exception: {e}")

        self.assertEqual(Meal.objects.filter(id=meal_id).first().name, 'Veganer Burger')

    """
    This test makes sure that attempting to update a non existing meal
    fails with an exception.
    """
    def test_update_missing_meal(self):
        meal_id = -999
        self.assertRaises(Exception, update_meal, meal_id, 'Sushi')
