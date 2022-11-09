from django.shortcuts import redirect, render
from reservations.forms import CreateReservationForm
from django.contrib import messages

def create_new_reservation(request):
    if request.method == "GET":
        context = {
            'form': CreateReservationForm
        }
        return render(request, 'reservations/create_new_reservation.html', context=context)
    if request.method == "POST":
        form = CreateReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Úspešne ste vytvorili novú rezerváciu.")
            return redirect("/")
        else:
            messages.error(request, "Pri validácii dát, ktoré ste zadali, nastala chyba. Skúste to znovu.")
            context = {
                "form": form
            }
            return render(request, 'reservations/create_new_reservation.html', context=context)