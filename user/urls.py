from django.urls import path
from .views import list_locations, register, login, insert_location

urlpatterns = [
    path('list/', list_locations),
    path('register/', register),
    path('login/', login),
    path('add/', insert_location)
]
