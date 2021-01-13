from django.urls import path, include
from .views import Handler

urlpatterns = [
    path('callback', Handler.as_view()),
]
