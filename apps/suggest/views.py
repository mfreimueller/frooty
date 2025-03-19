from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import plan_meals

"""
The API endpoint that predicts the next seven meals
(including an alternative for each meal) and returns
the generated results.
"""
@api_view(["POST"])
def suggest(request):
    next_meals = plan_meals()
    return Response({ "prediction": next_meals })
