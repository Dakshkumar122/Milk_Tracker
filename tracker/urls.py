from django.urls import path
from . import views

urlpatterns = [
    path('', views.milk_tracker, name='milk_tracker'),
]