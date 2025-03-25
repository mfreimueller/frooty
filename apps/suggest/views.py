from rest_framework.response import Response
from .services import plan_meals
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import authentication

class SuggestView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    The API endpoint that predicts the next seven meals
    (including an alternative for each meal) and returns
    the generated results.
    """
    def post(request):
        next_meals = plan_meals()
        return Response({ "prediction": next_meals })
