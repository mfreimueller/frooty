from rest_framework.response import Response
from .services import plan_meals
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import authentication
import datetime

class SuggestView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    The API endpoint that predicts the next seven meals
    (including an alternative for each meal) and returns
    the generated results.
    """
    def post(self, request):
        user = request.user
        data = request.data

        family_id = data.get('familyId')
        start_date_str = data.get('startDate')

        if not all([ family_id, start_date_str ]):
            return Response({ 'error': '`family_id` and `start_date` are required.' }, status=400)


        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()

        try:
            next_meals = plan_meals(user, family_id, start_date)
        except Exception as e:
            return Response({ 'error': e }, status=400)
        
        return Response({ "suggestions": next_meals })
