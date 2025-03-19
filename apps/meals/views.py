from rest_framework.views import APIView
from rest_framework.response import Response
from .services import add_meals, get_all_meals

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
        except:
            # at this point, either the database was locked or a meal wasn't found
            return Response({ 'error': 'Invalid request.' }, status=400)

        return Response({ 'meals': created_meals })

class MealUpdateDeleteView(APIView):
    def patch(self, request, meal_id):
        pass

    def delete(self, request, meal_id):
        pass
