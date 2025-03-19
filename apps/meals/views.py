from rest_framework.views import APIView
from rest_framework.response import Response
from .services import add_meal, delete_meal, get_all_meals, update_meal

class MealListCreateView(APIView):
    """
    GET /api/meals

    An API endpoint that returns all meal entries of the
    internal data storage.
    """
    def get(self, request):
        all_meals = get_all_meals()
        return Response({ "history": all_meals })

    """
    POST /api/meals

    An API endpoint that creates a new meal entry in
    the internal data storage to use for further predictions.
    """
    def post(self, request):
        data = request.data
        meals = data['meal']

        try:
            created_meal = add_meal(meals)
        except Exception as e:
            # at this point, either the database was locked or a meal wasn't found
            return Response({ 'error': e }, status=400)

        return Response({ 'meal': created_meal })

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
            return Response({ 'error': e }, status=400)

        return Response({}, status=200)

    """
    DELETE /api/meals/{meal_id}

    An API endpoint that deletes the meal with the given id.
    """
    def delete(self, request, meal_id):
        try:
            delete_meal(meal_id)
        except Exception as e:
            return Response({ 'error': e }, status=400)
        
        return Response({}, status=200)
