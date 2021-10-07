from django.urls import path
from . import views

# URL Conf
urlpatterns = [
    path('exercises/', views.exercises),
    path('hello/', views.say_hello)
]
