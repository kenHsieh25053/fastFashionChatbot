from django.urls import path
from .views import LineMessageController, ProfileController

urlpatterns = [
    path('callback', LineMessageController.as_view()),
    path('profile-form', ProfileController.as_view())
]
