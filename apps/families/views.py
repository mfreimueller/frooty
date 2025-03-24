from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .services import FamilyService
from django.contrib.auth.decorators import login_required

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
    def put(self, request, family_id):
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
    logged in user is its owner. TODO !!!
    """
    def delete(self, request, family_id):
        user = request.user

        try:
            FamilyService().delete_group(user, family_id)
        except Exception as e:
            return Response({ 'error': e }, status=400)
        
        return Response({}, status=200)


@login_required
@api_view(['POST'])
def add_to_group(request):
    data = request.data
    user = request.user

    group_name = data.get('name')
    user_name = data.get('user')
    if not all([ group_name, user_name ]):
        return Response({ 'error': 'Requires names of user and group.' }, status=400)
    
    try:
        add_user_to_group(user, group_name, user_name)
    except Exception as e:
        return Response({ 'error': e }, status=400)
    
    return Response({ 'success': True })

@login_required
@api_view(['DELETE'])
def remove_from_group(request):
    data = request.data
    user = request.user

    group_name = data.get('name')
    user_name = data.get('user')
    if not all([ group_name, user_name ]):
        return Response({ 'error': 'Requires names of user and group.' }, status=400)
    
    try:
        remove_user_from_group(user, group_name, user_name)
    except Exception as e:
        return Response({ 'error': e }, status=400)
    
    return Response({ 'success': True })
