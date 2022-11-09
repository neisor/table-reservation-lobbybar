from django.urls import path
from reservations.views import *

urlpatterns = [
    path('', create_new_reservation, name="create_new_reservation"),
]
