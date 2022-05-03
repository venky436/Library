from importlib.resources import Resource
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser,IsAuthenticated
# Create your views here.
# Response(serializer.data, status=status.HTTP_201_CREATED)
from .serializer import BookSerializer, UserSerializer,UserSerializerWithToken
from .models import Book
from django.contrib.auth.models import User
from django.contrib.auth.hashers import  make_password 


from django.contrib.auth import authenticate, login



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
#     def validate(self,attrs):

#         dat = super().validate(attrs)
#         try:
#             siri = UserSerializerWithToken(self.user).data
#             for k,v in siri.items():
#                dat[k] = v
#             return dat
#         except:
#             message = {
#                 'detail' : 'somthingwrong'
#             }
#             return Response(message,status=status.HTTP_400_BAD_REQUEST)

   
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer


# @api_view(['GET'])
# def user_details(request):
#     user = User.objects.all()
#     seri = UserSerializer(user,many=True)
#     return Response(seri.data)

# SIGNUP USER
@api_view(['POST'])
def create_user(request):
    data = request.data
    print(data['is_admin'])
    try:
        if data['is_admin'] == True:
            user = User.objects.create(
               username = data['email'],
               email = data['email'],
               password = make_password(data['password'])
            )
            user.is_staff = True
            user.save()
            seri = UserSerializerWithToken(user,many=False)
            return Response(seri.data)
        else:
            user = User.objects.create(
               username = data['username'],
               email = data['email'],
               password = make_password(data['password'])
            )
            seri = UserSerializerWithToken(user,many=False)
            return Response(seri.data)

    except:
        return Response('No data Enterd', status=status.HTTP_201_CREATED)

# LOGIN
@api_view(['POST'])
def user_login(request):
    data = request.data
    
    if request.user.is_staff != True:
        
        user = authenticate(request,username = data['username'],password = data['password'])
        if user is not None:
            login(request,user)
            seri = UserSerializerWithToken(user,many=False)
            return Response(seri.data)
        else:
            return Response('Admin User has to Login with Email')
    elif request.user.is_staff == True:
        user = User.objects.filter(email = data['email'],password = data['password'])
        if user is not None:
            login(request,user)
            seri = UserSerializerWithToken(user,many=False)
            return Response(seri.data)

    
        
    
 
# ALL BOOKS
@api_view(['GET'])
def Books(request):
    book = Book.objects.all()
    seri = BookSerializer(book,many=True)

    return Response(seri.data)

# ADD BOOK
@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_book(request):
    data = request.data
    book = Book.objects.create(user=request.user,name = data['name'])
    seri = BookSerializer(book,many=False)
    return Response(seri.data)

# UPDATE BOOK
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_book(request):
    data = request.data
    book = Book.objects.get(id = int(data['id']))
    book.name = data['name']
    book.save()
    seri = BookSerializer(book,many=False)
    return Response(seri.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def delete_book(request,pk):
    # data = request.data
    book = Book.objects.get(id = int(pk))
    book.delete()
    # seri = BookSerializer(book,many=False)
    return Response('Book Has Deleted Successfully')

    

