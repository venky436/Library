from django.urls import path

# JWT VIEWS
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    # TokenRefreshView,
)
from .views import Books,delete_book,create_user,update_book,add_book,user_login
urlpatterns = [
    # path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('books',Books),
    path('user/create',create_user),
    path('user_login',user_login),
    path('add_book',add_book),
    # ADMIN ACION
    path('update_book',update_book),
    path('delete_book/<str:pk>',delete_book),
    
]