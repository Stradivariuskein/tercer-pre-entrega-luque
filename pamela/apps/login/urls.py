from django.urls import path, include
from .views import *


urlpatterns = [
    path('login/', view_login, name= "login"),
    path('register/', Register.as_view(), name= "register"),
    path('register/acount/', register_acount, name= "acount"),
    path('logout/', user_logout, name= "logout"),
]
    
