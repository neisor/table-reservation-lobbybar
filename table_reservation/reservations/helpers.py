from django.core.mail import send_mail
from core.models import Reservation, AdminEmail, NepovolenyDatum, KontaktneTelefonneCislo, Aktivita, NepovolenaAktivitaNaDatum
from django.urls import reverse
import datetime
from django.db.models import QuerySet

def get_available_aktivity_for_a_date(date: datetime.date) -> QuerySet:
    """Gets all of the available Aktivita instances for today."""
    if isinstance(date, str):
        # Convert to datetime.date
        date = datetime.datetime.strptime(date, '%d.%m.%Y').date()
    not_allowed_ids_of_activities_for_today = NepovolenaAktivitaNaDatum.objects.filter(datum=date).values_list('aktivita__id', flat=True)
    allowed_activities_for_today = Aktivita.objects.exclude(id__in=not_allowed_ids_of_activities_for_today)
    return allowed_activities_for_today

def check_if_datum_from_reservation_is_in_nepovolene_datumy(date_to_check: datetime.date) -> bool:
    """Returns True (boolean) if date exists in NepovolenyDatum - therefore the reservation should not be created"""
    exists_in_nepovolene_datumy = True if NepovolenyDatum.objects.all().filter(datum=date_to_check) else False
    return exists_in_nepovolene_datumy

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

    Sme radi, že si sa rozhodol stráviť večer s nami v Lobby Bar!

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

    Tím Lobby Bar
    """
    html_message = f"""
    <b>Hola Amigo!</b><br/><br/>

    Sme radi, že si sa rozhodol stráviť večer s nami v <b>Lobby Bar</b>!<br/><br/>

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

    <i>Tím Lobby Bar</i>
    """
    admin_email = AdminEmail.objects.all().first()
    if admin_email:
        send_mail(
            subject='Lobby Bar - Potvrďťe Vašu rezerváciu',
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
    if admin_email:
        send_mail(
            subject=f'Lobby Bar - Nová rezervácia - ID: {reservation.id}',
            message=plain_text_message,
            from_email=admin_email.email,
            recipient_list=[admin_email.email],
            html_message=html_message,
            fail_silently=False,
        )
    return


def notify_customer_about_accepted_or_declined_reservation(reservation: Reservation) -> None:
    kontaktne_cislo = KontaktneTelefonneCislo.objects.all().first()
    if kontaktne_cislo:
        contact_tel_number = kontaktne_cislo.telefonne_cislo
    else:
        contact_tel_number = "+421 xxx xxx xxx"  # Just in cases when no KontaktneTelefonneCislo has been created yet

    if reservation.stav == Reservation.Stavy.PRIJATA:
        subject = "Lobby Bar - Rezervácia prijatá"
        message_text = "Tvoja rezervácia bola PRIJATÁ!"
        html_message_text = "Tvoja rezervácia bola <b>PRIJATÁ</b>!"
        signature_html_text = "Ďakujeme, že si si vybral <b>Lobby Bar</b>!"
        signature_text = "Ďakujeme, že si si vybral Lobby Bar!"
    else:
        subject = "Lobby Bar - Rezervácia zamietnutá"
        message_text = """Mrzí nás to, ale tvoja rezervácia bola ZAMIETNUTÁ!
        Prosím, skontroluj detaily tvojej rezervácie a skúsime to spoločne napraviť!
        """
        html_message_text = """
        Mrzí nás to, ale tvoja rezervácia bola <b>ZAMIETNUTÁ</b>!<br/><br/>
        <b>Prosím, skontroluj detaily tvojej rezervácie a skúsime to spoločne napraviť!</b>
        """
        signature_html_text = "Ďakujeme!"
        signature_text = "Ďakujeme!"
    aktivity = get_only_nazov_for_each_aktivita_from_reservation(reservation)
    plain_text_message = f"""
    Hola Amigo!
    
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

    V prípade akéhokoľvek problému nás, prosím, kontaktujte na tel. čísle: {contact_tel_number}

    {signature_text}
    Muchas gracias!

    Tím Lobby Bar
    """
    html_message = f"""
    Hola Amigo!<br/><br/>
    
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

    V prípade akéhokoľvek problému nás, prosím, kontaktujte na tel. čísle: <a href="tel:{contact_tel_number}">{contact_tel_number}</a><br/><br/>

    {signature_html_text}<br/>
    <b>Muchas gracias!</b><br/><br/>

    <i>Tím Lobby Bar</i>
    """
    admin_email = AdminEmail.objects.all().first()
    if admin_email:
        send_mail(
            subject=subject,
            message=plain_text_message,
            from_email=admin_email.email,
            recipient_list=[reservation.email],
            html_message=html_message,
            fail_silently=False,
        )
    return
