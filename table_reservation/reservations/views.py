from django.shortcuts import redirect, render
from reservations.forms import CreateReservationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from reservations.helpers import *
from core.models import Reservation, PovolenyCas
import uuid

def create_new_reservation(request):
    if request.method == "GET":
        povoleny_cas = PovolenyCas.objects.all().first()
        context = {
            'form': CreateReservationForm,
            'povoleny_cas': povoleny_cas
        }
        return render(request, 'reservations/create_new_reservation.html', context=context)
    if request.method == "POST":
        form = CreateReservationForm(request.POST)
        if form.is_valid():
            created_reservation = form.save()
            created_reservation.stav = Reservation.Stavy.NOVA
            created_reservation.save()
            messages.success(request, "Úspešne ste vytvorili novú rezerváciu.")
        else:
            messages.error(request, "Pri validácii dát, ktoré ste zadali, nastala chyba. Skúste to znovu.")
            context = {
                "form": form
            }
            return render(request, 'reservations/create_new_reservation.html', context=context)
        generate_and_send_new_reservation_email_to_customer(request=request, reservation=created_reservation)
        return redirect("/")

def confirm_reservation_by_user(request, reservation_uuid4: uuid.UUID):
    reservation = Reservation.objects.filter(uuid_identificator=reservation_uuid4).first()
    if not reservation:
        messages.warning(request, f'Zadaná rezervácia neexistuje.')
        return redirect("/")
    reservation.stav = Reservation.Stavy.EMAILOVA_ADRESA_POTVRDENA
    reservation.save()
    messages.success(request, 'Rezervácia bola úspešne potvrdená. O prijatí rezervácie budete informovaní e-mailom.')
    notify_administrator_to_accept_or_decline_reservation(request=request, reservation=reservation)
    return redirect("/")

@login_required
def accept_reservation(request, reservation_uuid4: uuid.UUID):
    reservation = Reservation.objects.filter(uuid_identificator=reservation_uuid4).first()
    if not reservation:
        messages.warning(request, f'Zadaná rezervácia neexistuje.')
        return redirect("all_reservations")
    if reservation.stav in [Reservation.Stavy.CAKA_SA_NA_POTVRDENIE_EMAILOVEJ_ADRESY, Reservation.Stavy.NOVA]:
        messages.error(request, "Rezervácia nemôže byť potvrdená predtým, ako zákazník potvrdí svoju rezerváciu cez e-mail.")
        return redirect("all_reservations")
    if reservation.stav in [Reservation.Stavy.POTVRDENA, Reservation.Stavy.ZAMIETNUTA]:
        messages.error(request, f"Zadaná rezervácia už bola potvrdená alebo zamietnutá v minulosti.")
        return redirect("all_reservations")
    reservation.stav = Reservation.Stavy.POTVRDENA
    reservation.save()
    # SEND ACCEPTANCE EMAIL TO THE CUSTOMER
    notify_customer_about_accepted_or_declined_reservation(reservation=reservation)
    messages.success(request, f"Rezervácia číslo {reservation.id} bola úspešne prijatá.")
    return redirect("all_reservations")

@login_required
def decline_reservation(request, reservation_uuid4: uuid.UUID):
    reservation = Reservation.objects.filter(uuid_identificator=reservation_uuid4).first()
    if not reservation:
        messages.warning(request, f'Zadaná rezervácia neexistuje.')
        return redirect("all_reservations")
    if reservation.stav in [Reservation.Stavy.CAKA_SA_NA_POTVRDENIE_EMAILOVEJ_ADRESY, Reservation.Stavy.NOVA]:
        messages.error(request, "Rezervácia nemôže byť zamietnutá predtým, ako zákazník potvrdí svoju rezerváciu cez e-mail.")
        return redirect("all_reservations")
    if reservation.stav in [Reservation.Stavy.POTVRDENA, Reservation.Stavy.ZAMIETNUTA]:
        messages.error(request, f"Zadaná rezervácia už bola potvrdená alebo zamietnutá v minulosti.")
        return redirect("all_reservations")
    reservation.stav = Reservation.Stavy.ZAMIETNUTA
    reservation.save()
    # SEND DECLINATION EMAIL TO THE CUSTOMER
    notify_customer_about_accepted_or_declined_reservation(reservation=reservation)
    messages.success(request, f"Rezervácia číslo {reservation.id} bola zamietnutá.")
    return redirect("all_reservations")

@login_required
def all_reservations(request):
    all_reservations = Reservation.objects.all().order_by('-id')  # Ordered by id since the id is always last id + 1
    context = {
        'all_reservations': all_reservations
    }
    return render(request, 'reservations/all_reservations.html', context=context)
