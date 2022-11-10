from django.urls import path
from reservations.views import *

urlpatterns = [
    path('all', all_reservations, name="all_reservations"),
    path('', create_new_reservation, name="create_new_reservation"),
    path('confirm/<uuid:reservation_uuid4>', confirm_reservation_by_user, name="confirm_reservation_by_user"),
]
