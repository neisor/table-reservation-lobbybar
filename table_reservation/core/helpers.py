from django.core.mail import send_mail
from core.models import AdminEmail

def send_email_notification_system_closed_to_admin() -> None:
    plain_text_message = f"""
    Rezervačný systém bol zatvorený. Zákazníci aktuálne nebudú môcť vytvárať nové rezervácie.
    Môžete ho Vy, ako administrátor, znovu otvoriť priamo cez rezervačný systém.    
    """
    html_message = f"""
    Rezervačný systém bol zatvorený. Zákazníci aktuálne nebudú môcť vytvárať nové rezervácie.<br/>
    Môžete ho Vy, ako administrátor, znovu otvoriť priamo cez rezervačný systém.    
    """
    admin_email = AdminEmail.objects.all().first()
    if admin_email:
        send_mail(
            subject='Lobby Bar - Stav systému zmenený na ZATVORENÝ',
            message=plain_text_message,
            from_email=admin_email.email,
            recipient_list=[admin_email.email],
            html_message=html_message,
            fail_silently=False,
        )
    return

def send_email_notification_system_opened_to_admin() -> None:
    plain_text_message = f"""
    Rezervačný systém bol otvorený. Zákazníci už budú môcť vytvárať nové rezervácie.
    Môžete ho Vy, ako administrátor, znovu zatvoriť priamo cez rezervačný systém.    
    """
    html_message = f"""
    Rezervačný systém bol zatvorený. Zákazníci aktuálne nebudú môcť vytvárať nové rezervácie.<br/>
    Môžete ho Vy, ako administrátor, znovu zatvoriť priamo cez rezervačný systém.    
    """
    admin_email = AdminEmail.objects.all().first()
    if admin_email:
        send_mail(
            subject='Lobby Bar - Stav systému zmenený na OTVORENÝ',
            message=plain_text_message,
            from_email=admin_email.email,
            recipient_list=[admin_email.email],
            html_message=html_message,
            fail_silently=False,
        )
    return