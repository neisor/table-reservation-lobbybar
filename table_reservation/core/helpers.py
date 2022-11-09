from django.core.mail import send_mail
from core.models import Reservation

def generate_and_send_new_reservation_email_to_customer(request, reservation: Reservation) -> None:
    html_text = f"""
    Dobrý deň,
    Vašu rezerváciu je potrebné potvrdiť.

    Detaily rezervácie
    Počet ľudí:
    Dátum:
    Čas:

    Pre potvrdenie Vašej rezervácie stlačte nasledovný link:

    """
    return
