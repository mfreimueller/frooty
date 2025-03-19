from rest_framework.views import APIView
from rest_framework.response import Response
from .services import add_meals, get_all_meals, update_meal

class MealListCreateView(APIView):
    """
    An API endpoint that returns all meal entries of the
    internal data storage.
    """
    def get(self, request):
        all_meals = get_all_meals()
        return Response({ "history": all_meals })

    """
    An API endpoint that creates new meal entries in
    the internal data storage to use for further predictions.
    The meal entries are appended to the storage and are
    treated as the latest elements.
    """
    def post(self, request):
        data = request.data
        meals = data['meals']

        try:
            created_meals = add_meals(meals)
        except Exception as e:
            # at this point, either the database was locked or a meal wasn't found
            return Response({ 'error': e }, status=400)

        return Response({ 'meals': created_meals })

class MealUpdateDeleteView(APIView):
    """
    PUT /api/meals/{meal_id}

    An API endpoint that updates the meal with the given id.
    The idea is to allow the user to change meals in retrospect
    in order to have the stored data represent the actual meal plan
    for further suggestions.
    """
    def put(self, request, meal_id):
        data = request.data

        if 'meal' not in data:
            return Response({ 'error': 'Excepted `meal` parameter.' }, status=400)

        meal = data['meal']

        try:
            update_meal(meal_id, meal)
        except Exception as e:
            # either the ID was invalid or the meal wasn't found
            if hasattr(e, 'message'):
                return Response({ 'error': e }, status=400)
            else:
                return Response({ 'error': 'Invalid request.' }, status=400)

        return Response({}, status=200)

    def delete(self, request, meal_id):
        pass
