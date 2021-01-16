from django.urls import path
from .views import Controller

urlpatterns = [
    path('callback', Controller.as_view()),
]
