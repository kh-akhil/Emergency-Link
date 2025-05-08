from .views import locations, alert, test
from django.urls import path

urlpatterns = [
    path('list/', locations),
    path('alert/', alert),
    path('test/', test)
]
