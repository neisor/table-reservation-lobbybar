from django.urls import path
from core.views import *

urlpatterns = [
    path('povoleny-cas/all', all_povolene_casy, name="all_povolene_casy"),
    path('povoleny-cas/new', create_new_povoleny_cas, name="create_new_povoleny_cas"),
    path('povoleny-cas/edit/<int:povoleny_cas_id>', edit_povoleny_cas, name="edit_povoleny_cas"),
    path('povoleny-cas/delete/<int:povoleny_cas_id>', delete_povoleny_cas, name="delete_povoleny_cas"),
]
