from django.core.mail import send_mail
from core.models import Reservation
from django.urls import reverse

def generate_and_send_new_reservation_email_to_customer(request, reservation: Reservation) -> None:
    url_to_confirm_reservation = request.build_absolute_uri(reverse('confirm_reservation_by_user', args=(reservation.uuid_identificator, )))
    plain_text_message = f"""
    Dobrý deň,
    Vašu rezerváciu je potrebné potvrdiť kliknutím na nižšie uvedený odkaz.

    Detaily Vašej rezervácie:
    Počet ľudí: {reservation.pocet_ludi}
    Dátum: {reservation.datum.strftime("%d.%m.%Y")}
    Čas: {reservation.cas.strftime("%H:%M")}
    Meno: {reservation.meno}
    Priezvisko: {reservation.priezvisko}
    Tel. č.: {reservation.telefonne_cislo}
    E-mail: {reservation.email}

    Pre potvrdenie Vašej rezervácie stlačte nasledovný odkaz:

    {url_to_confirm_reservation}

    (Skopírujte vyššie uvedený odkaz a vložte ho do prehliadača.)

    Bez Vášho potvrdenia rezervácie nebude možné Vašu rezerváciu prijať.
    """ 
    send_mail(
        'El Nacional - Rezervácia',
        plain_text_message,
        [reservation.email],
        fail_silently=False,
    )
    return
