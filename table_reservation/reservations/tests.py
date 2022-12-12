from django.test import LiveServerTestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.test import Client
from reservations.views import *
from core.models import Reservation, Stav
from unittest.mock import patch
import datetime as dt
import uuid
from django.contrib.messages.storage.fallback import FallbackStorage

# Create your tests here.
class TestReservations(LiveServerTestCase):
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
        self.uuid_identificator = uuid.uuid4()
        Reservation(
            uuid_identificator=self.uuid_identificator,
            meno="Tester",
            priezvisko="Testovsky",
            datum=dt.datetime.now().date() + dt.timedelta(days=1),
            cas=dt.time(hour=18, minute=30),
            telefonne_cislo="0911222333",
            email="test@test.com",
            stav=Reservation.Stavy.NOVA
        ).save()
        self.reservation = Reservation.objects.get(uuid_identificator=self.uuid_identificator)
        self.stav = Stav.objects.create(otvorene=True)
        self.stav.save()

    def _set_reservation_stav(self, reservation_uuid4, stav):
        reservation_to_test = Reservation.objects.get(uuid_identificator=reservation_uuid4)
        reservation_to_test.stav = stav
        reservation_to_test.save()
        return

    def test_reservation_view(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        # Add support for Django messages in tests
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = create_new_reservation(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nová žiadosť o rezerváciu")
    
    def test_reservation_view_closed_system(self):
        self.stav.otvorene = not self.stav.otvorene
        self.stav.save()
        request = self.factory.get('/')
        request.user = AnonymousUser()
        # Add support for Django messages in tests
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        response = create_new_reservation(request)
        # Revert Stav before assertions
        self.stav.otvorene = not self.stav.otvorene
        self.stav.save()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aktuálne nie je možné vytvárať nové rezervácie")

    def test_all_reservations_view(self):
        request = self.factory.get('/all')
        request.user = self.user
        response = all_reservations(request)
        response.client = Client()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Všetky rezervácie")

    def test_no_access_to_all_reservations_for_unauthorized_user(self):
        request = self.factory.get('/all')
        request.user = AnonymousUser()
        response = all_reservations(request)
        response.client = Client()
        self.assertRedirects(response, '/accounts/login/?next=/all', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_no_access_to_show_message_for_unauthorized_user(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = show_message_from_user(request)
        response.client = Client()
        self.assertRedirects(response, '/accounts/login/?next=/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    @patch('reservations.views.notify_administrator_to_accept_or_decline_reservation')
    def test_confirm_reservation_by_user(self, mock_send_email_method):
        request = Client().get(f'/confirm/{str(self.reservation.uuid_identificator)}', follow=True)
        # Add support for Django messages in tests
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        request.user = AnonymousUser()
        response = confirm_reservation_by_user(request, self.reservation.uuid_identificator)
        reservation_modified = Reservation.objects.get(uuid_identificator=self.reservation.uuid_identificator)
        self.assertEqual(reservation_modified.stav, Reservation.Stavy.EMAILOVA_ADRESA_POTVRDENA)

    @patch('reservations.views.notify_customer_about_accepted_or_declined_reservation')
    def test_accept_reservation(self, mock_send_email_method):
        self._set_reservation_stav(self.reservation.uuid_identificator, Reservation.Stavy.EMAILOVA_ADRESA_POTVRDENA)
        request = Client().get(f'/accept/{str(self.reservation.uuid_identificator)}', follow=True)
        # Add support for Django messages in tests
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        request.user = self.user
        response = accept_reservation(request, self.reservation.uuid_identificator)
        reservation_modified = Reservation.objects.get(uuid_identificator=self.reservation.uuid_identificator)
        self.assertEqual(reservation_modified.stav, Reservation.Stavy.PRIJATA)

    @patch('reservations.views.notify_customer_about_accepted_or_declined_reservation')
    def test_decline_reservation(self, mock_send_email_method):
        self._set_reservation_stav(self.reservation.uuid_identificator, Reservation.Stavy.EMAILOVA_ADRESA_POTVRDENA)
        request = Client().get(f'/decline/{str(self.reservation.uuid_identificator)}', follow=True)
        # Add support for Django messages in tests
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        request.user = self.user
        response = decline_reservation(request, self.reservation.uuid_identificator)
        reservation_modified = Reservation.objects.get(uuid_identificator=self.reservation.uuid_identificator)
        self.assertEqual(reservation_modified.stav, Reservation.Stavy.ZAMIETNUTA)

    def test_fail_to_accept_reservation_from_wrong_initial_stav(self):
        self._set_reservation_stav(self.reservation.uuid_identificator, Reservation.Stavy.NOVA)
        request = Client().get(f'/accept/{str(self.reservation.uuid_identificator)}', follow=True)
        # Add support for Django messages in tests
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        request.user = self.user
        response = accept_reservation(request, self.reservation.uuid_identificator)
        reservation_modified = Reservation.objects.get(uuid_identificator=self.reservation.uuid_identificator)
        self.assertEqual(reservation_modified.stav, Reservation.Stavy.NOVA)

    def test_fail_to_decline_reservation_from_wrong_initial_stav(self):
        self._set_reservation_stav(self.reservation.uuid_identificator, Reservation.Stavy.NOVA)
        request = Client().get(f'/decline/{str(self.reservation.uuid_identificator)}', follow=True)
        # Add support for Django messages in tests
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))
        request.user = self.user
        response = decline_reservation(request, self.reservation.uuid_identificator)
        reservation_modified = Reservation.objects.get(uuid_identificator=self.reservation.uuid_identificator)
        self.assertEqual(reservation_modified.stav, Reservation.Stavy.NOVA)
    