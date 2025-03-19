from rest_framework.views import APIView
from rest_framework.response import Response

class HistoryListCreateView(APIView):
    """
    GET /api/history

    An API endpoint that returns all history entries of the
    internal data storage.
    """
    def get(self, request):
        pass

    """
    POST /api/history

    An API endpoint that creates new history entries in
    the internal data storage to use for further predictions.
    The history entries are appended to the storage and are
    treated as the latest (and most recent) elements.
    """
    def post(self, request):
        pass

class HistoryUpdateDeleteView(APIView):
    """
    PUT /api/history/{history_id}

    An API endpoint that updates the history with the given id.
    The idea is to allow the user to change the history in retrospect
    in order to have the stored data represent the actual meal plan
    for further suggestions.
    """
    def put(self, request, history_id):
        pass

    """
    DELETE /api/history/{history_id}

    An API endpoint that deletes the history item with the given id.
    """
    def delete(self, request, history_id):
        pass
