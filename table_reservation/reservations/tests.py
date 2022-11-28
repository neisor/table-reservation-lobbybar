from django.test import LiveServerTestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.test import Client
from reservations.views import *

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

    def test_reservation_view(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = create_new_reservation(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nová žiadosť o rezerváciu")

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
