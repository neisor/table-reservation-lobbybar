from django.shortcuts import redirect, render
from reservations.forms import CreateReservationForm
from django.contrib import messages
from core.helpers import generate_and_send_new_reservation_email_to_customer
from core.models import Reservation
import uuid

def create_new_reservation(request):
    if request.method == "GET":
        context = {
            'form': CreateReservationForm
        }
        return render(request, 'reservations/create_new_reservation.html', context=context)
    if request.method == "POST":
        form = CreateReservationForm(request.POST)
        if form.is_valid():
            created_reservation = form.save()
            messages.success(request, "Úspešne ste vytvorili novú rezerváciu.")
            # return redirect("/")
        else:
            messages.error(request, "Pri validácii dát, ktoré ste zadali, nastala chyba. Skúste to znovu.")
            context = {
                "form": form
            }
            return render(request, 'reservations/create_new_reservation.html', context=context)
        generate_and_send_new_reservation_email_to_customer(request=request, reservation=created_reservation)
        return redirect("/")

def confirm_reservation_by_user(request, reservation_uuid4: uuid.UUID):
    reservation = Reservation.objects.filter(uuid_identificator=reservation_uuid4)
    if not reservation:
        messages.warning(request, f'Zadaná rezervácia neexistuje.')
    return redirect("/")

def accept_reservation(request):
    pass

def decline_reservation(request):
    pass

def all_reservations(request):
    pass
