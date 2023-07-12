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
    path('nepovolena-aktivita-pre-datum/all', all_nepovolene_aktivity_pre_datumy, name="all_nepovolene_aktivity_pre_datumy"),
    path('nepovolena-aktivita-pre-datum/new', create_new_nepovolena_aktivita_pre_datum, name="create_new_nepovolena_aktivita_pre_datum"),
    path('nepovolena-aktivita-pre-datum/delete/<int:nepovolena_aktivita_pre_datum_id>', delete_nepovolena_aktivita_pre_datum, name="delete_nepovolena_aktivita_pre_datum"),
    path('stav/new', create_new_stav_systemu, name="create_new_stav_systemu"),
    path('stav/actual-stav-systemu', actual_stav_systemu, name="actual_stav_systemu"),
    path('stav/open-or-close-system', open_or_close_system, name="open_or_close_system"),
    path('nepovoleny-datum/create', create_new_nepovoleny_datum, name="create_new_nepovoleny_datum"),
    path('nepovoleny-datum/all', all_nepovolene_datumy, name="all_nepovolene_datumy"),
    path('nepovoleny-datum/delete/<int:nepovoleny_datum_id>', delete_nepovoleny_datum, name="delete_nepovoleny_datum"),
    path('kontaktne-cislo/create', create_new_kontaktne_cislo, name="create_new_kontaktne_cislo"),
    path('kontaktne-cislo/all', all_kontaktne_cisla, name="all_kontaktne_cisla"),
    path('kontaktne-cislo/delete/<int:kontaktne_cislo_id>', delete_kontaktne_cislo, name="delete_kontaktne_cislo"),
]
