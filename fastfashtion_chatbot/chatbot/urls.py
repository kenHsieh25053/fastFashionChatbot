from django.urls import path
from .views import LineMessageController, ProfileController
from django.views.generic import TemplateView

urlpatterns = [
    path('callback', LineMessageController.as_view()),
    path('profile-form', TemplateView.as_view(template_name='profile-form0.html')),
    path('profile-form/<str:userid>', ProfileController.as_view()),
]
