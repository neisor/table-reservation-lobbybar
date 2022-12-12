from django.test import LiveServerTestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import Client
from django.urls import reverse
from core.models import *
import datetime as dt
import uuid
from core.views import *
from unittest.mock import patch

class TestCore(LiveServerTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            'admin',
            'change-me@change-me.com',
            'passwo123412'
        )
        self.user.is_staff=True
        self.user.is_superuser=True
        self.user.is_admin=True
        self.user.save()
        self.stav = Stav.objects.create(otvorene=True)
        self.stav.save()

    def create_povoleny_cas_and_return_id(self) -> int:
        povoleny_cas = PovolenyCas(
            cas_rezervacii_od=dt.time(hour=15),
            cas_rezervacii_do=dt.time(hour=21)
        )
        povoleny_cas.save()
        return povoleny_cas.id
    
    def create_aktivita_and_return_id(self) -> int:
        aktivita = Aktivita(nazov="Test aktivita")
        aktivita.save()
        return aktivita.id

    def create_admin_email_and_return_id(self) -> int:
        admin_email = AdminEmail(email="admin@some_domain.com")
        admin_email.save()
        return admin_email.id

    def test_create_instance_of_Reservation(self):
        Reservation(
            uuid_identificator=uuid.uuid4(),
            meno="Tester",
            priezvisko="Testovsky",
            datum=dt.datetime.now().date() + dt.timedelta(days=1),
            cas=dt.time(hour=18, minute=30),
            telefonne_cislo="0911222333",
            email="test@test.com",
            stav=Reservation.Stavy.NOVA
        ).save()
        assert Reservation.objects.exists()

    def test_create_instance_of_Aktivita(self):
        Aktivita(id=1, nazov="Test aktivita").save()
        assert Aktivita.objects.exists()

    def test_create_instance_of_PovolenyCas(self):
        PovolenyCas(
            id=1,
            cas_rezervacii_od=dt.time(hour=15),
            cas_rezervacii_do=dt.time(hour=21)
        ).save()
        assert PovolenyCas.objects.exists()
        with self.assertRaises(ValidationError):
            PovolenyCas(
                cas_rezervacii_od=dt.time(hour=15),
                cas_rezervacii_do=dt.time(hour=21)
            ).save()

    def test_create_instance_of_AdminEmail(self):
        AdminEmail(id=1, email="admin@some_domain.com").save()
        assert AdminEmail.objects.exists()
        with self.assertRaises(ValidationError):
                    AdminEmail(email="admin2@some_domain2.com").save()

    # Unauthenticated tests:        
    def test_no_access_to_all_povolene_casy_for_unauthorized_user(self):
        request = self.factory.get('/povoleny-cas/all')
        request.user = AnonymousUser()
        response = all_povolene_casy(request)
        response.client = Client()
        self.assertRedirects(response, '/accounts/login/?next=/povoleny-cas/all', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_no_access_to_create_new_povoleny_cas_for_unauthorized_user(self):
        request = self.factory.get('/povoleny-cas/new')
        request.user = AnonymousUser()
        response = create_new_povoleny_cas(request)
        response.client = Client()
        self.assertRedirects(response, '/accounts/login/?next=/povoleny-cas/new', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_no_access_to_edit_povoleny_cas_for_unauthorized_user(self):
        request = self.factory.get('/povoleny-cas/edit/1')
        request.user = AnonymousUser()
        response = edit_povoleny_cas(request)
        response.client = Client()
        self.assertRedirects(response, '/accounts/login/?next=/povoleny-cas/edit/1', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_no_access_to_delete_povoleny_cas_for_unauthorized_user(self):
        request = self.factory.get('/povoleny-cas/delete/1')
        request.user = AnonymousUser()
        response = delete_povoleny_cas(request)
        response.client = Client()
        self.assertRedirects(response, '/accounts/login/?next=/povoleny-cas/delete/1', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_no_access_to_all_admin_emaily_for_unauthorized_user(self):
        request = self.factory.get('/admin-email/all')
        request.user = AnonymousUser()
        response = all_admin_emaily(request)
        response.client = Client()
        self.assertRedirects(response, '/accounts/login/?next=/admin-email/all', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_no_access_to_create_new_admin_email_for_unauthorized_user(self):
        request = self.factory.get('/admin-email/new')
        request.user = AnonymousUser()
        response = create_new_admin_email(request)
        response.client = Client()
        self.assertRedirects(response, '/accounts/login/?next=/admin-email/new', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_no_access_to_delete_povoleny_cas_for_unauthorized_user(self):
        request = self.factory.get('/admin-email/delete/1')
        request.user = AnonymousUser()
        response = delete_admin_email(request)
        response.client = Client()
        self.assertRedirects(response, '/accounts/login/?next=/admin-email/delete/1', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_no_access_to_all_aktivity_for_unauthorized_user(self):
        request = self.factory.get('/aktivita/all')
        request.user = AnonymousUser()
        response = all_aktivity(request)
        response.client = Client()
        self.assertRedirects(response, '/accounts/login/?next=/aktivita/all', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_no_access_to_create_new_aktivita_for_unauthorized_user(self):
        request = self.factory.get('/aktivita/new')
        request.user = AnonymousUser()
        response = create_new_aktivita(request)
        response.client = Client()
        self.assertRedirects(response, '/accounts/login/?next=/aktivita/new', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_no_access_to_edit_aktivita_for_unauthorized_user(self):
        request = self.factory.get('/aktivita/edit/1')
        request.user = AnonymousUser()
        response = edit_aktivita(request)
        response.client = Client()
        self.assertRedirects(response, '/accounts/login/?next=/aktivita/edit/1', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_no_access_to_delete_aktivita_for_unauthorized_user(self):
        request = self.factory.get('/aktivita/delete/1')
        request.user = AnonymousUser()
        response = delete_aktivita(request)
        response.client = Client()
        self.assertRedirects(response, '/accounts/login/?next=/aktivita/delete/1', status_code=302, target_status_code=200, fetch_redirect_response=True)

    # Authenticated tests:
    def test_all_povolene_casy(self):
        request = self.factory.get('/povoleny-cas/all')
        request.user = self.user
        response = all_povolene_casy(request)
        response.client = Client()
        self.assertContains(response, "Všetky povolené časy")

    def test_create_new_povoleny_cas(self):
        request = self.factory.get('/povoleny-cas/new')
        request.user = self.user
        response = create_new_povoleny_cas(request)
        response.client = Client()
        self.assertContains(response, "Nový povolený čas")

    def test_edit_povoleny_cas(self):
        instance_id = self.create_povoleny_cas_and_return_id()
        request = self.factory.get(f'/povoleny-cas/edit/{str(instance_id)}')
        request.user = self.user
        # Add support for Django messages in tests
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = edit_povoleny_cas(request, instance_id)
        response.client = Client()
        self.assertContains(response, "Zmeniť povolený čas")

    def test_delete_povoleny_cas(self):
        instance_id = self.create_povoleny_cas_and_return_id()
        request = self.factory.get(f'/povoleny-cas/delete/{str(instance_id)}')
        request.user = self.user
        # Add support for Django messages in tests
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = delete_povoleny_cas(request, instance_id)
        response.client = Client()
        self.assertRedirects(response, reverse('all_povolene_casy'), status_code=302, target_status_code=302, fetch_redirect_response=True)

    def test_all_admin_emaily(self):
        request = self.factory.get('/admin-email/all')
        request.user = self.user
        response = all_admin_emaily(request)
        response.client = Client()
        self.assertContains(response, "Všetky administrátorské e-maily")

    def test_create_new_admin_email(self):
        request = self.factory.get('/admin-email/new')
        request.user = self.user
        response = create_new_admin_email(request)
        response.client = Client()
        self.assertContains(response, "Nový administrátorský e-mail")

    def test_delete_admin_email(self):
        instance_id = self.create_admin_email_and_return_id()
        request = self.factory.get(f'/admin-email/delete/{str(instance_id)}')
        request.user = self.user
        # Add support for Django messages in tests
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = delete_admin_email(request, instance_id)
        response.client = Client()
        self.assertRedirects(response, reverse('all_admin_emaily'), status_code=302, target_status_code=302, fetch_redirect_response=True)

    def test_all_aktivity(self):
        request = self.factory.get('/aktivita/all')
        request.user = self.user
        response = all_aktivity(request)
        response.client = Client()
        self.assertContains(response, "Všetky aktivity")

    def test_create_new_aktivita(self):
        request = self.factory.get('/aktivita/new')
        request.user = self.user
        response = create_new_aktivita(request)
        response.client = Client()
        self.assertContains(response, "Nová aktivita")

    def test_edit_aktivita(self):
        instance_id = self.create_aktivita_and_return_id()
        request = self.factory.get(f'/aktivita/edit/{str(instance_id)}')
        request.user = self.user
        # Add support for Django messages in tests
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = edit_aktivita(request, instance_id)
        response.client = Client()
        self.assertContains(response, "Zmeniť aktivitu")

    def test_delete_aktivita(self):
        instance_id = self.create_aktivita_and_return_id()
        request = self.factory.get(f'/aktivita/delete/{str(instance_id)}')
        request.user = self.user
        # Add support for Django messages in tests
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = delete_aktivita(request, instance_id)
        response.client = Client()
        self.assertRedirects(response, reverse('all_aktivity'), status_code=302, target_status_code=302, fetch_redirect_response=True)

class TestStav(LiveServerTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            'admin',
            'change-me@change-me.com',
            'passwo123412'
        )
        self.user.is_staff=True
        self.user.is_superuser=True
        self.user.is_admin=True
        self.user.save()
        self.stav = Stav.objects.create(otvorene=True)
        self.stav.save()

    def test_create_new_stav_already_existing(self):
        request = self.factory.get('/stav/new')
        request.user = self.user
        # Add support for Django messages in tests
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = create_new_stav_systemu(request)
        response.client = Client()
        self.assertRedirects(response, reverse('actual_stav_systemu'), status_code=302, target_status_code=302, fetch_redirect_response=True)

    @patch('core.views.send_email_notification_system_closed_to_admin')
    def test_change_stav_systemu(self, mock_send_email_notification):
        request = self.factory.get('/stav/open-or-close-system')
        request.user = self.user
        # Add support for Django messages in tests
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = open_or_close_system(request)
        response.client = Client()
        self.assertRedirects(response, reverse('actual_stav_systemu'), status_code=302, target_status_code=302, fetch_redirect_response=True)
