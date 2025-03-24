from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import add_user_to_group, authenticate_user, create_new_group, logout_user, register_user, remove_user_from_group, update_user_password
from django.contrib.auth.decorators import login_required

@api_view(['POST'])
def register(request):
    data = request.data

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([ username, email, password ]):
        return Response({ 'error': 'Requires username, email and password.' }, status=400)

    try:
        register_user(username, email, password)
    except Exception as e:
        return Response({ 'error': e }, status=400)

    return Response({ 'success': True })

@api_view(['POST'])
def authenticate(request):
    data = request.data

    username = data.get('username')
    password = data.get('password')

    if not all([ username, password ]):
        return Response({ 'error': 'Requires username and password.' }, status=400)
    
    if authenticate_user(request, username, password):
        return Response({ 'success': True })
    else:
        return Response({ 'error': 'Username and/or password invalid.' }, status=400)

@api_view(['POST'])
def logout(request):
    if logout_user(request):
        return Response({ 'success': True })
    else:
        return Response({ 'error': 'Failed to log user out.' }, status=400)

@login_required
@api_view(['PUT'])
def update_password(request):
    data = request.data
    user = request.user

    password = data.get('password')
    if password is None:
        return Response({ 'error': 'Requires password.' }, status=400)
    
    update_user_password(user, password)
    return Response({ 'success': True })

@login_required
@api_view(['POST'])
def create_group(request):
    data = request.data
    user = request.user

    group_name = data.get('name')
    if group_name is None:
        return Response({ 'error': 'Requires name of group.' }, status=400)
    
    group = create_new_group(user, group_name)
    return Response({ 'group': group })

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
