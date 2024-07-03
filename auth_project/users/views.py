from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

def authenticate_user(id):
  payload = {
      'id': id,
      'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
      'iat': datetime.datetime.utcnow()
    }
  token = jwt.encode(payload , 'secret' , algorithm='HS256').decode('utf-8')
  response = Response()
  response.set_cookie(key='jwt', value=token, httponly= True) #Cant Be Accessed through js to prevent any attack 
  response.data = {
    'jwt': token
  }
  return response


class RegisterView(APIView):
  def post(self, request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response = authenticate_user(serializer.data['id'])
    return response

class LoginView(APIView):
  def post(self, request):
    email = request.data['email']
    password = request.data['password']

    user = User.objects.filter(email=email).first() #as email is unique so we get first one 
    if user is None:
      raise AuthenticationFailed('User Not Found!')
    
    if not user.check_password(password):
      raise AuthenticationFailed('Password is not correct.')
    
    response = authenticate_user(user.id)
    return response
  

class UserView(APIView):
  def get(self, request):
    token = request.COOKIES.get('jwt')

    if not token:
      raise AuthenticationFailed('Unauthenticated')
    
    try:
      payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('Unauthenticated')
    
    user = User.objects.filter(id = payload['id']).first()
    serializer = UserSerializer(user)
    return Response(serializer.data)
  
"""
# Not Usable as when we delete the cookie from the response it will be found on the client device again
# so He will send it again.
class LogoutView(APIView):
  def post(self, request):
    response = Response()
    response.delete_cookie()
    response.data = {
      'message': 'Logout Success'
    }
    return response
"""
