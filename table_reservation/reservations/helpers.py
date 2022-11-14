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
    Hola Amigo!
    Sme radi, že si sa rozhodol stráviť večer s nami v EL NACIONAL!

    Nezabudni potvrdiť svoju rezerváciu kliknutím na nasledujúci odkaz, inak bude tvoja rezervácia neplatná:
    {url_to_confirm_reservation}

    Detail tvojej rezervácie:
    Počet ľudí: {reservation.pocet_ludi}
    Dátum: {reservation.datum.strftime("%d.%m.%Y")}
    Čas: {reservation.cas.strftime("%H:%M")}
    Aktivity: {aktivity}
    Meno: {reservation.meno}
    Priezvisko: {reservation.priezvisko}
    Tel. č.: {reservation.telefonne_cislo}
    E-mail: {reservation.email}
    Správa: {reservation.sprava if reservation.sprava else '-'}

    Hneď ako tvoju rezerváciu spracujeme, pošleme ti potvrdzujúci e-mail.

    Ďakujeme!
    Muchas gracias!

    Tím El Nacional
    """
    html_message = f"""
    <b>Hola Amigo!</b><br/>
    Sme radi, že si sa rozhodol stráviť večer s nami v <b>EL NACIONAL</b>!<br/><br/>

    <b>Nezabudni potvrdiť svoju rezerváciu kliknutím na nasledujúci odkaz, inak bude tvoja rezervácia neplatná:</b><br/>
    <a href="{url_to_confirm_reservation}">{url_to_confirm_reservation}</a><br/><br/>

    <b>Detail tvojej rezervácie:</b><br/>
    <b>Počet ľudí:</b> {reservation.pocet_ludi}<br/>
    <b>Dátum:</b> {reservation.datum.strftime("%d.%m.%Y")}<br/>
    <b>Čas:</b> {reservation.cas.strftime("%H:%M")}<br/>
    <b>Aktivity:</b> {aktivity}<br/>
    <b>Meno:</b> {reservation.meno}<br/>
    <b>Priezvisko:</b> {reservation.priezvisko}<br/>
    <b>Tel. č.:</b> {reservation.telefonne_cislo}<br/>
    <b>E-mail:</b> {reservation.email}<br/>
    <b>Správa:</b> {reservation.sprava if reservation.sprava else '-'}<br/><br/>

    Hneď ako tvoju rezerváciu spracujeme, pošleme ti potvrdzujúci e-mail.<br/><br/>

    Ďakujeme!<br/>
    <b>Muchas gracias!</b><br/><br/>

    <i>Tím El Nacional</i>
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

    Pre <b>PRIJATIE</b> rezervácie stlačte nasledovný odkaz:<br/>
    <a href="{url_to_accept_reservation}">{url_to_accept_reservation}</a><br/><br/>

    Pre <b>ZAMIETNUTIE</b> rezervácie stlačte nasledovný odkaz:<br/>
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
        message_text = "Tvoja rezervácia bola PRIJATÁ!"
        html_message_text = "Tvoja rezervácia bola <b>PRIJATÁ</b>!"
        signature_html_text = "Ďakujeme, že si si vybral <b>EL NACIONAL</b>!"
        signature_text = "Ďakujeme, že si si vybral EL NACIONAL!"
    else:
        subject = "El Nacional - Rezervácia zamietnutá"
        message_text = """Tvoja rezervácia bola ZAMIETNUTÁ!
        Prosím, skontroluj detaily tvojej rezervácie a skúsime to spoločne napraviť!
        """
        html_message_text = """
        Tvoja rezervácia bola <b>ZAMIETNUTÁ</b>!<br/><br/>
        <b>Prosím, skontroluj detaily tvojej rezervácie a skúsime to spoločne napraviť!</b>
        """
        signature_html_text = "Ďakujeme!"
        signature_text = "Ďakujeme!"
    aktivity = get_only_nazov_for_each_aktivita_from_reservation(reservation)
    plain_text_message = f"""
    Dobrý deň,
    
    {message_text}
    
    Detaily tvojej rezervácie:
    Počet ľudí: {reservation.pocet_ludi}
    Dátum: {reservation.datum.strftime("%d.%m.%Y")}
    Čas: {reservation.cas.strftime("%H:%M")}
    Aktivity: {aktivity}
    Meno: {reservation.meno}
    Priezvisko: {reservation.priezvisko}
    Tel. č.: {reservation.telefonne_cislo}
    E-mail: {reservation.email}
    Správa: {reservation.sprava if reservation.sprava else '-'}

    V prípade akéhokoľvek problému nás, prosím, kontaktujte na tel. čísle: +421 903 470 561

    {signature_text}
    Muchas gracias!
    Tím El Nacional
    """
    html_message = f"""
    Dobrý deň,<br/><br/>
    
    {html_message_text}<br/><br/>
    
    <b>Detaily tvojej rezervácie:</b><br/>
    <b>Počet ľudí:</b> {reservation.pocet_ludi}<br/>
    <b>Dátum:</b> {reservation.datum.strftime("%d.%m.%Y")}<br/>
    <b>Čas:</b> {reservation.cas.strftime("%H:%M")}<br/>
    <b>Aktivity:</b> {aktivity}<br/>
    <b>Meno:</b> {reservation.meno}<br/>
    <b>Priezvisko:</b> {reservation.priezvisko}<br/>
    <b>Tel. č.:</b> {reservation.telefonne_cislo}<br/>
    <b>E-mail:</b> {reservation.email}<br/>
    <b>Správa:</b> {reservation.sprava if reservation.sprava else '-'}<br/><br/>

    V prípade akéhokoľvek problému nás, prosím, kontaktujte na tel. čísle: <a href="tel:+421903470561">+421 903 470 561</a><br/><br/>

    {signature_html_text}<br/>
    <b>Muchas gracias!</b><br/>
    <i>Tím El Nacional</i>
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
