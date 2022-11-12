from django.urls import path
from reservations.views import *

urlpatterns = [
    path('all', all_reservations, name="all_reservations"),
    path('', create_new_reservation, name="create_new_reservation"),
    path('confirm/<uuid:reservation_uuid4>', confirm_reservation_by_user, name="confirm_reservation_by_user"),
    path('accept/<uuid:reservation_uuid4>', accept_reservation, name="accept_reservation"),
    path('decline/<uuid:reservation_uuid4>', decline_reservation, name="decline_reservation"),
    path('edit-poznamka-administratora/<uuid:reservation_uuid4>', edit_or_show_poznamka_administratora, name="edit_or_show_poznamka_administratora"),
    path('show-message/<uuid:reservation_uuid4>', show_message_from_user, name="show_message_from_user"),
]
