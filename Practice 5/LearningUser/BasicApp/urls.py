from django.urls import path
from BasicApp import  views

app_name = "BasicApp"

urlpatterns = [
    path("user_login", views.user_login , name = "user_login"),
    path("Register", views.Register , name = "Register"),
]
