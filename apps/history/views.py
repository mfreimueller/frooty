from rest_framework.views import APIView
from rest_framework.response import Response
from .services import HistoryService
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication

class HistoryListCreateView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    """
    GET /api/history

    An API endpoint that returns all history entries of the
    internal data storage.
    """
    def get(self, request):
        user = request.user

        family_id = request.query_params['family_id']
        if family_id is None:
            return Response({ 'error': 'family_id is required.' }, status=400)
        
        try:
            history_of_family = HistoryService().get_all_of_family(user, family_id)
        except Exception as e:
            return Response({ 'error': e }, status=400)
        
        return Response({ 'history': history_of_family })

    """
    POST /api/history

    An API endpoint that creates new history entries in
    the internal data storage to use for further predictions.
    The history entries are appended to the storage and are
    treated as the latest (and most recent) elements.
    """
    def post(self, request):
        user = request.user
        data = request.data

        history = data.get('history')

        if history is None:
            return Response({ 'error': '`history` is required.' }, status=400)
        
        try:
            historyItems = HistoryService().add_history(user, history)
        except Exception as e:
            return Response({ 'error': repr(e) }, status=400)

        return Response({ 'history': historyItems })

class HistoryUpdateDeleteView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    """
    PUT /api/history/{history_id}

    An API endpoint that updates the history with the given id.
    The idea is to allow the user to change the history in retrospect
    in order to have the stored data represent the actual meal plan
    for further suggestions.
    """
    def put(self, request, history_id):
        user = request.user
        data = request.data

        meal = data.get('meal')

        if meal is None:
            return Response({ 'error': '`meal` is required.' }, status=400)
        
        try:
            HistoryService().update_history_item(user, history_id, meal)
        except Exception as e:
            return Response({ 'error': e }, status=400)
        
        return Response({ 'success': True })

    """
    DELETE /api/history/{history_id}

    An API endpoint that deletes the history item with the given id.
    """
    def delete(self, request, history_id):
        user = request.user
        data = request.data

        try:
            HistoryService().delete_history_item(user, history_id)
        except Exception as e:
            return Response({ 'error': e }, status=400)
        
        return Response({ 'success': True })
