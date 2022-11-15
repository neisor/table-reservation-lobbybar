from django.shortcuts import redirect, render
from reservations.forms import *
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from reservations.helpers import *
from core.models import Reservation, PovolenyCas
import uuid
from django.core.paginator import Paginator

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
            messages.success(request, "Úspešne ste vytvorili novú rezerváciu. Je potrebné aby ste potvrdili rezerváciu na Vami zadanej e-mailovej adrese.")
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
        messages.error(request, "Rezervácia nemôže byť prijatá predtým, ako zákazník potvrdí svoju rezerváciu cez e-mail.")
        return redirect("all_reservations")
    # # Do not allow changing reservation's stav once it has been accepted or rejected
    # if reservation.stav in [Reservation.Stavy.PRIJATA, Reservation.Stavy.ZAMIETNUTA]:
    #     messages.error(request, f"Zadaná rezervácia už bola prijatá alebo zamietnutá v minulosti.")
    #     return redirect("all_reservations")
    reservation.stav = Reservation.Stavy.PRIJATA
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
    # # Do not allow changing reservation's stav once it has been accepted or rejected
    # if reservation.stav in [Reservation.Stavy.PRIJATA, Reservation.Stavy.ZAMIETNUTA]:
    #     messages.error(request, f"Zadaná rezervácia už bola prijatá alebo zamietnutá v minulosti.")
    #     return redirect("all_reservations")
    reservation.stav = Reservation.Stavy.ZAMIETNUTA
    reservation.save()
    # SEND DECLINATION EMAIL TO THE CUSTOMER
    notify_customer_about_accepted_or_declined_reservation(reservation=reservation)
    messages.success(request, f"Rezervácia číslo {reservation.id} bola zamietnutá.")
    return redirect("all_reservations")

@login_required
def all_reservations(request):
    search_value = request.GET.get('search')
    if search_value:
        try:
            search_value_uuid = uuid.UUID(search_value)  # Try to convert search string to UUID
        except ValueError:
            search_value_uuid = uuid.UUID(int=1)
        try:
            search_value_id = int(search_value)  # Try to convert search string to integer
        except ValueError:
            search_value_id = 0
        all_reservations = Reservation.objects.all() \
            .filter(
                Q(id=search_value_id) | Q(uuid_identificator=search_value_uuid) | Q(meno__icontains=search_value) | Q(priezvisko__icontains=search_value) | \
                Q(sprava__icontains=search_value) | Q(telefonne_cislo__icontains=search_value) | Q(email__icontains=search_value)
            ) \
            .order_by('-id')  # Ordered by id since the id is always last id + 1 (so it's by the newest reservations)
    else:
        all_reservations = Reservation.objects.all().order_by('-id')  # Ordered by id since the id is always last id + 1
    number_of_reservations_per_page = 25 # Show 25 reservations per page.
    if request.GET.get("zobrazitVsetko"):
        context = {"all_reservations": all_reservations}
        return render(request, 'reservations/all_reservations.html', context=context)
    else:
        paginator = Paginator(all_reservations, number_of_reservations_per_page)
        page_number = request.GET.get('page', 1)
        all_reservations = page_obj = paginator.get_page(page_number)
        context = {
            "all_reservations": all_reservations,
            "page_obj": page_obj,
            "number_of_reservations_per_page": number_of_reservations_per_page
        }
    return render(request, 'reservations/all_reservations.html', context=context)


@login_required
def edit_or_show_poznamka_administratora(request, reservation_uuid4: uuid.UUID):
    reservation = Reservation.objects.all().filter(uuid_identificator=reservation_uuid4).first()
    if not reservation:
        messages.warning(request, f'Zadaná rezervácia v systéme neexistuje.')
        return redirect("all_reservations")
    if request.method == "GET":
        form = EditPoznamkaAdministratora(instance=reservation)
        context = {
            'form': form,
            "reservation": reservation
        }
        return render(request, 'reservations/edit_poznamka_administratora.html', context=context)
    if request.method == "POST":
        form = EditPoznamkaAdministratora(data=request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, f"Úspešne ste pridali poznámku k rezervácii s ID {reservation.id}.")
        else:
            messages.error(request, "Pri validácii dát, ktoré ste zadali, nastala chyba. Skúste to znovu.")
            context = {
                "form": form,
                "reservation": reservation
            }
            return render(request, 'reservations/edit_poznamka_administratora.html', context=context)
        return redirect("all_reservations")

@login_required
def show_message_from_user(request, reservation_uuid4: uuid.UUID):
    reservation = Reservation.objects.all().filter(uuid_identificator=reservation_uuid4).first()
    if not reservation:
        messages.warning(request, f'Zadaná rezervácia v systéme neexistuje.')
        return redirect("all_reservations")
    if not reservation.sprava:
        messages.warning(request, f'Zadaná rezervácia neobsahuje žiadnu správu.')
        return redirect("all_reservations")
    context = {
        "reservation": reservation
    }
    return render(request, 'reservations/show_message_from_user.html', context=context)
