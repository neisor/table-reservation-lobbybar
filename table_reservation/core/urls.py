from django.urls import path
from core.views import *

urlpatterns = [
    path('povoleny-cas/all', all_povolene_casy, name="all_povolene_casy"),
    path('povoleny-cas/new', create_new_povoleny_cas, name="create_new_povoleny_cas"),
    path('povoleny-cas/edit/<int:povoleny_cas_id>', edit_povoleny_cas, name="edit_povoleny_cas"),
    path('povoleny-cas/delete/<int:povoleny_cas_id>', delete_povoleny_cas, name="delete_povoleny_cas"),
    path('admin-email/all', all_admin_emaily, name="all_admin_emaily"),
    path('admin-email/new', create_new_admin_email, name="create_new_admin_email"),
    path('admin-email/delete/<int:admin_email_id>', delete_admin_email, name="delete_admin_email"),
    path('aktivita/all', all_aktivity, name="all_aktivity"),
    path('aktivita/new', create_new_aktivita, name="create_new_aktivita"),
    path('aktivita/edit/<int:aktivita_id>', edit_aktivita, name="edit_aktivita"),
    path('aktivita/delete/<int:aktivita_id>', delete_aktivita, name="delete_aktivita"),
    path('stav/new', create_new_stav_systemu, name="create_new_stav_systemu"),
    path('stav/actual-stav-systemu', actual_stav_systemu, name="actual_stav_systemu"),
    path('stav/open-or-close-system', open_or_close_system, name="open_or_close_system"),
]
