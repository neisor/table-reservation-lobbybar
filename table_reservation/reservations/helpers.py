from django.core.mail import send_mail
from core.models import Reservation, AdminEmail
from django.urls import reverse

def get_only_nazov_for_each_aktivita_from_reservation(reservation: Reservation) -> str:
    aktivity_z_rezervacie = ""
    for aktivita in reservation.aktivita.all():
        aktivity_z_rezervacie += aktivita.nazov + ", "
    aktivity_z_rezervacie = aktivity_z_rezervacie.rstrip(", ")
    return aktivity_z_rezervacie

def generate_and_send_new_reservation_email_to_customer(request, reservation: Reservation) -> None:
    url_to_confirm_reservation = request.build_absolute_uri(reverse('confirm_reservation_by_user', args=(reservation.uuid_identificator, )))
    aktivity = get_only_nazov_for_each_aktivita_from_reservation(reservation)
    plain_text_message = f"""
    Dobrý deň,
    Vašu rezerváciu je pred vybavením potrebné potvrdiť kliknutím na nižšie uvedený odkaz.

    Detaily Vašej rezervácie:
    Počet ľudí: {reservation.pocet_ludi}
    Dátum: {reservation.datum.strftime("%d.%m.%Y")}
    Čas: {reservation.cas.strftime("%H:%M")}
    Aktivity: {aktivity}
    Meno: {reservation.meno}
    Priezvisko: {reservation.priezvisko}
    Tel. č.: {reservation.telefonne_cislo}
    E-mail: {reservation.email}
    Správa: {reservation.sprava if reservation.sprava else '-'}

    Pre potvrdenie Vašej rezervácie stlačte nasledovný odkaz:

    {url_to_confirm_reservation}

    (Skopírujte vyššie uvedený odkaz a vložte ho do prehliadača v prípade nefunkčnosti automatického prekliku.)

    Bez Vášho potvrdenia rezervácie nebude možné Vašu rezerváciu prijať.

    UPOZORNENIE: Po prijatí alebo zamietnutí rezervácie Vám príde potvrdzujúci e-mail.

    Ďakujeme.
    Tím El Nacional
    https://elnacional.sk
    """
    html_message = f"""
    Dobrý deň,<br/>
    Vašu rezerváciu je pred vybavením potrebné potvrdiť kliknutím na nižšie uvedený odkaz.<br/><br/>

    <b>Detaily Vašej rezervácie:</b><br/>
    <b>Počet ľudí:</b> {reservation.pocet_ludi}<br/>
    <b>Dátum:</b> {reservation.datum.strftime("%d.%m.%Y")}<br/>
    <b>Čas:</b> {reservation.cas.strftime("%H:%M")}<br/>
    <b>Aktivity:</b> {aktivity}<br/>
    <b>Meno:</b> {reservation.meno}<br/>
    <b>Priezvisko:</b> {reservation.priezvisko}<br/>
    <b>Tel. č.:</b> {reservation.telefonne_cislo}<br/>
    <b>E-mail:</b> {reservation.email}<br/>
    <b>Správa:</b> {reservation.sprava if reservation.sprava else '-'}<br/><br/>

    Pre potvrdenie Vašej rezervácie stlačte nasledovný odkaz:<br/>
    <a href="{url_to_confirm_reservation}">{url_to_confirm_reservation}</a><br/><br/>

    (Skopírujte vyššie uvedený odkaz a vložte ho do prehliadača v prípade nefunkčnosti automatického prekliku.)<br/><br/>

    Bez Vášho potvrdenia rezervácie nebude možné Vašu rezerváciu prijať.<br/><br/>

    <b>UPOZORNENIE:</b> Po prijatí alebo zamietnutí rezervácie Vám príde potvrdzujúci e-mail.<br/><br/>

    Ďakujeme.<br/>
    Tím El Nacional<br/>
    <a href="https://elnacional.sk">https://elnacional.sk</a>
    """
    admin_email = AdminEmail.objects.all().first()
    send_mail(
        subject='El Nacional - Potvrďťe Vašu rezerváciu',
        message=plain_text_message,
        from_email=admin_email.email,
        recipient_list=[reservation.email],
        html_message=html_message,
        fail_silently=False,
    )
    return

def notify_administrator_to_accept_or_decline_reservation(request, reservation: Reservation) -> None:
    url_to_accept_reservation = request.build_absolute_uri(reverse('accept_reservation', args=(reservation.uuid_identificator, )))
    url_to_decline_reservation = request.build_absolute_uri(reverse('decline_reservation', args=(reservation.uuid_identificator, )))
    aktivity = get_only_nazov_for_each_aktivita_from_reservation(reservation)
    plain_text_message = f"""
    Dobrý deň,
    
    Existuje nová rezervácia na potvrdenie alebo zamietnutie.
    
    Detaily novej rezervácie:
    Počet ľudí: {reservation.pocet_ludi}
    Dátum: {reservation.datum.strftime("%d.%m.%Y")}
    Čas: {reservation.cas.strftime("%H:%M")}
    Aktivity: {aktivity}
    Meno: {reservation.meno}
    Priezvisko: {reservation.priezvisko}
    Tel. č.: {reservation.telefonne_cislo}
    E-mail: {reservation.email}
    Správa: {reservation.sprava if reservation.sprava else '-'}

    Pre prijatie rezervácie stlačte nasledovný odkaz:
    {url_to_accept_reservation}

    Pre zamietnutie rezervácie stlačte nasledovný odkaz:
    {url_to_decline_reservation}

    (Skopírujte vyššie uvedený odkaz a vložte ho do prehliadača v prípade nefunkčnosti automatického prekliku.)
    """
    html_message = f"""
    Dobrý deň,<br/><br/>
    
    Existuje nová rezervácia na potvrdenie alebo zamietnutie.<br/>
    
    <b><u>Detaily novej rezervácie:</u></b><br/>
    <b>Počet ľudí:</b> {reservation.pocet_ludi}<br/>
    <b>Dátum:</b> {reservation.datum.strftime("%d.%m.%Y")}<br/>
    <b>Čas:</b> {reservation.cas.strftime("%H:%M")}<br/>
    <b>Aktivity:</b> {aktivity}<br/>
    <b>Meno:</b> {reservation.meno}<br/>
    <b>Priezvisko:</b> {reservation.priezvisko}<br/>
    <b>Tel. č.:</b> {reservation.telefonne_cislo}<br/>
    <b>E-mail:</b> {reservation.email}<br/>
    <b>Správa:</b> {reservation.sprava if reservation.sprava else '-'}<br/><br/>

    Pre <b>prijatie</b> rezervácie stlačte nasledovný odkaz:<br/>
    <a href="{url_to_accept_reservation}">{url_to_accept_reservation}</a><br/><br/>

    Pre <b>zamietnutie</b> rezervácie stlačte nasledovný odkaz:<br/>
    <a href="{url_to_decline_reservation}">{url_to_decline_reservation}</a><br/><br/>

    (Skopírujte vyššie uvedený odkaz a vložte ho do prehliadača v prípade nefunkčnosti automatického prekliku.)
    """
    admin_email = AdminEmail.objects.all().first()
    send_mail(
        subject=f'El Nacional - Nová rezervácia - ID: {reservation.id}',
        message=plain_text_message,
        from_email=admin_email.email,
        recipient_list=[admin_email.email],
        html_message=html_message,
        fail_silently=False,
    )
    return


def notify_customer_about_accepted_or_declined_reservation(reservation: Reservation) -> None:
    if reservation.stav == Reservation.Stavy.PRIJATA:
        subject = "El Nacional - Rezervácia prijatá"
        message_text = "Vaša rezervácia bola PRIJATÁ! Tešíme sa na Vás."
    else:
        subject = "El Nacional - Rezervácia zamietnutá"
        message_text = "Vaša rezervácia bola ZAMIETNUTÁ!"
    aktivity = get_only_nazov_for_each_aktivita_from_reservation(reservation)
    plain_text_message = f"""
    Dobrý deň,
    
    {message_text}
    
    Detaily Vašej rezervácie:
    Počet ľudí: {reservation.pocet_ludi}
    Dátum: {reservation.datum.strftime("%d.%m.%Y")}
    Čas: {reservation.cas.strftime("%H:%M")}
    Aktivity: {aktivity}
    Meno: {reservation.meno}
    Priezvisko: {reservation.priezvisko}
    Tel. č.: {reservation.telefonne_cislo}
    E-mail: {reservation.email}
    Správa: {reservation.sprava if reservation.sprava else '-'}

    Ďakujeme.
    Tím El Nacional
    https://elnacional.sk
    """
    html_message = f"""
    Dobrý deň,<br/><br/>
    
    {message_text}<br/><br/>
    
    <b><u>Detaily Vašej rezervácie:</u></b><br/>
    <b>Počet ľudí:</b> {reservation.pocet_ludi}<br/>
    <b>Dátum:</b> {reservation.datum.strftime("%d.%m.%Y")}<br/>
    <b>Čas:</b> {reservation.cas.strftime("%H:%M")}<br/>
    <b>Aktivity:</b> {aktivity}<br/>
    <b>Meno:</b> {reservation.meno}<br/>
    <b>Priezvisko:</b> {reservation.priezvisko}<br/>
    <b>Tel. č.:</b> {reservation.telefonne_cislo}<br/>
    <b>E-mail:</b> {reservation.email}<br/>
    <b>Správa:</b> {reservation.sprava if reservation.sprava else '-'}<br/><br/>

    Ďakujeme.<br/>
    Tím El Nacional<br/>
    <a href="https://elnacional.sk">https://elnacional.sk</a>
    """
    admin_email = AdminEmail.objects.all().first()
    send_mail(
        subject=subject,
        message=plain_text_message,
        from_email=admin_email.email,
        recipient_list=[reservation.email],
        html_message=html_message,
        fail_silently=False,
    )
    return
