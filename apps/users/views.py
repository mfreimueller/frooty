from rest_framework.response import Response
from rest_framework.decorators import api_view
from .services import authenticate_user, logout_user, register_user, update_user_password
from django.contrib.auth.decorators import login_not_required

@login_not_required
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

@login_not_required
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

@api_view(['PUT'])
def update_password(request):
    data = request.data
    user = request.user

    password = data.get('password')
    if password is None:
        return Response({ 'error': 'Requires password.' }, status=400)
    
    update_user_password(user, password)
    return Response({ 'success': True })
