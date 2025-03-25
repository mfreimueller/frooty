from rest_framework.response import Response
from .services import register_user, update_user_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import authentication

class RegisterUserView(APIView):
    def post(request):
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

class ManageUserView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(request):
        data = request.data
        user = request.user

        password = data.get('password')
        if password is None:
            return Response({ 'error': 'Requires password.' }, status=400)
        
        update_user_password(user, password)
        return Response({ 'success': True })
    
    def delete(request):
        pass # TODO !!!
