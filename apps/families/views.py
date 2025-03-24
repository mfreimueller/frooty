from rest_framework.response import Response
from rest_framework.views import APIView
from .services import FamilyService

class FamilyListCreateView(APIView):
    """
    GET /api/families

    Get all families associated with the current user.
    """
    def get(self, request):
        user = request.user

        all_groups = FamilyService().get_all_of_user(user)
        return Response({ "groups": all_groups })
    
    """
    POST /api/families
    """
    def post(self, request):
        data = request.data
        user = request.user

        family_name = data.get('name')
        if family_name is None:
            return Response({ 'error': 'Requires name of family.' }, status=400)
        
        family = FamilyService().create_family(user, family_name)
        return Response({ 'family': family })

class FamilyUpdateDeleteView(APIView):
    """
    PUT /api/families/{family_id}
    
    Updates the user visible family name.
    """
    def put(self, request, family_id: int):
        user = request.user
        data = request.data

        new_family_name = data.get('family_name')
        if new_family_name is None:
            return Response({ 'error': 'Excepted `family_name` parameter.' }, status=400)

        try:
            FamilyService().update_group(user, family_id, new_family_name)
        except Exception as e:
            return Response({ 'error': e }, status=400)

        return Response({}, status=200)

    """
    DELETE /api/families/{family_id}

    An API endpoint that deletes the family with the given id iff the
    logged in user is its owner.
    """
    def delete(self, request, family_id):
        user = request.user

        try:
            FamilyService().delete_group(user, family_id)
        except Exception as e:
            return Response({ 'error': e }, status=400)
        
        return Response({}, status=200)

class FamilyUserModifyView(APIView):
    """
    PUT /api/families/{family_id}/{user_name}
    
    Adds a user to the group.
    """
    def put(self, request, family_id: int, user_name: str):
        user = request.user

        try:
            FamilyService().add_user(user, family_id, user_name)
        except Exception as e:
            return Response({ 'error': e }, status=400)

        return Response({}, status=200)

    """
    DELETE /api/families/{family_id}/{user_name}

    Removes an user from the the group.
    """
    def delete(self, request, family_id, user_name: str):
        user = request.user

        try:
            FamilyService().remove_user(user, family_id, user_name)
        except Exception as e:
            return Response({ 'error': e }, status=400)
        
        return Response({}, status=200)
