from django.urls import path
from .views import RegisterUser,login_user,logout_user


urlpatterns = [
    path('register/',RegisterUser,name='register-user'),
    path('login/',login_user,name='login-user'),
    path('logout/',logout_user,name='logout_user'),
]