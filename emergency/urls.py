from .views import locations, alert
from django.urls import path

urlpatterns = [
    path('list/', locations),
    path('alert/', alert)
]
