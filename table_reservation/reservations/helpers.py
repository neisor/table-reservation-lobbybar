from django.core.mail import send_mail
from core.models import Reservation, AdminEmail
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

    (Skopírujte vyššie uvedený odkaz a vložte ho do prehliadača v prípade nefunkčnosti automatického prekliku.)

    Bez Vášho potvrdenia rezervácie nebude možné Vašu rezerváciu prijať.
    """
    html_message = f"""
    Dobrý deň,
    Vašu rezerváciu je potrebné potvrdiť kliknutím na nižšie uvedený odkaz.

    <b>Detaily Vašej rezervácie:</b>
    <b>Počet ľudí:</b> {reservation.pocet_ludi}
    <b>Dátum:</b> {reservation.datum.strftime("%d.%m.%Y")}
    <b>Čas:</b> {reservation.cas.strftime("%H:%M")}
    <b>Meno:</b> {reservation.meno}
    <b>Priezvisko:</b> {reservation.priezvisko}
    <b>Tel. č.:</b> {reservation.telefonne_cislo}
    <b>E-mail:</b> {reservation.email}

    Pre potvrdenie Vašej rezervácie stlačte nasledovný odkaz:
    <a href="{url_to_confirm_reservation}">{url_to_confirm_reservation}</a>

    (Skopírujte vyššie uvedený odkaz a vložte ho do prehliadača v prípade nefunkčnosti automatického prekliku.)

    Bez Vášho potvrdenia rezervácie nebude možné Vašu rezerváciu prijať.
    """
    recipient = AdminEmail.objects.all().first()
    send_mail(
        'El Nacional - Potvrďťe Vašu rezerváciu',
        plain_text_message,
        [recipient.email],
        html_message=html_message,
        fail_silently=False,
    )
    return

def notify_administrator_to_accept_or_decline_reservation(request, reservation: Reservation) -> None:
    url_to_accept_reservation = request.build_absolute_uri(reverse('accept_reservation', args=(reservation.uuid_identificator, )))
    url_to_decline_reservation = request.build_absolute_uri(reverse('decline_reservation', args=(reservation.uuid_identificator, )))
    plain_text_message = f"""
    Dobrý deň,
    
    Existuje nová rezervácia na potvrdenie alebo zamietnutie.
    
    Detaily novej rezervácie:
    Počet ľudí: {reservation.pocet_ludi}
    Dátum: {reservation.datum.strftime("%d.%m.%Y")}
    Čas: {reservation.cas.strftime("%H:%M")}
    Meno: {reservation.meno}
    Priezvisko: {reservation.priezvisko}
    Tel. č.: {reservation.telefonne_cislo}
    E-mail: {reservation.email}

    Pre prijatie rezervácie stlačte nasledovný odkaz:
    {url_to_accept_reservation}

    Pre zamietnutie rezervácie stlačte nasledovný odkaz:
    {url_to_decline_reservation}

    (Skopírujte vyššie uvedený odkaz a vložte ho do prehliadača v prípade nefunkčnosti automatického prekliku.)
    """
    html_message = f"""
    Dobrý deň,
    
    Existuje nová rezervácia na potvrdenie alebo zamietnutie.
    
    <b><u>Detaily novej rezervácie:</u></b>
    <b>Počet ľudí:</b> {reservation.pocet_ludi}
    <b>Dátum:</b> {reservation.datum.strftime("%d.%m.%Y")}
    <b>Čas:</b> {reservation.cas.strftime("%H:%M")}
    <b>Meno:</b> {reservation.meno}
    <b>Priezvisko:</b> {reservation.priezvisko}
    <b>Tel. č.:</b> {reservation.telefonne_cislo}
    <b>E-mail:</b> {reservation.email}

    Pre <b>prijatie</b> rezervácie stlačte nasledovný odkaz:
    <a href="{url_to_accept_reservation}">{url_to_accept_reservation}</a>

    Pre <b>zamietnutie</b> rezervácie stlačte nasledovný odkaz:
    <a href="{url_to_accept_reservation}">{url_to_decline_reservation}</a>

    (Skopírujte vyššie uvedený odkaz a vložte ho do prehliadača v prípade nefunkčnosti automatického prekliku.)
    """
    recipient = AdminEmail.objects.all().first()
    send_mail(
        f'El Nacional - Nová rezervácia - ID: {reservation.id}',
        plain_text_message,
        [recipient.email],
        html_message=html_message,
        fail_silently=False,
    )
    return