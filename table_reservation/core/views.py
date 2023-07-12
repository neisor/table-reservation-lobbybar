from django.shortcuts import render, redirect
from core.forms import *
from core.models import PovolenyCas, AdminEmail, Aktivita, Stav, NepovolenaAktivitaNaDatum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.helpers import *

@login_required
def all_povolene_casy(request):
    povolene_casy = PovolenyCas.objects.all()
    context = {
        "povolene_casy": povolene_casy
    }
    return render(request, 'core/all_povolene_casy.html', context=context)

@login_required
def create_new_povoleny_cas(request):
    if request.method == "GET":
        povoleny_cas = PovolenyCas.objects.all().first()
        if povoleny_cas:
            messages.warning(request, 'Povolený čas už existuje, nemôžete vytvoriť ďalší.')
            return redirect("all_povolene_casy")
        context = {
            'form': CreatePovolenyCasForm,
        }
        return render(request, 'core/create_new_povoleny_cas.html', context=context)
    if request.method == "POST":
        form = CreatePovolenyCasForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Úspešne ste vytvorili nový povolený čas.")
        else:
            messages.error(request, "Pri validácii dát, ktoré ste zadali, nastala chyba. Skúste to znovu.")
            context = {
                "form": form
            }
            return render(request, 'core/create_new_povoleny_cas.html', context=context)
        return redirect("all_povolene_casy")


@login_required
def edit_povoleny_cas(request, povoleny_cas_id: int):
    povoleny_cas = PovolenyCas.objects.all().filter(id=povoleny_cas_id).first()
    if not povoleny_cas:
        messages.warning(request, f'Povolený čas s ID {povoleny_cas_id} neexistuje.')
        return redirect("all_povolene_casy")
    if request.method == "GET":
        form = EditPovolenyCasForm(instance=povoleny_cas)
        context = {
            'form': form,
            "povoleny_cas": povoleny_cas
        }
        return render(request, 'core/edit_povoleny_cas.html', context=context)
    if request.method == "POST":
        form = EditPovolenyCasForm(data=request.POST, instance=povoleny_cas)
        if form.is_valid():
            form.save()
            messages.success(request, "Úspešne ste zmenili povolený čas.")
        else:
            messages.error(request, "Pri validácii dát, ktoré ste zadali, nastala chyba. Skúste to znovu.")
            context = {
                "form": form,
                "povoleny_cas": povoleny_cas
            }
            return render(request, 'core/edit_povoleny_cas.html', context=context)
        return redirect("all_povolene_casy")

@login_required
def delete_povoleny_cas(request, povoleny_cas_id: int):
    povoleny_cas = PovolenyCas.objects.all().filter(id=povoleny_cas_id).first()
    if not povoleny_cas:
        messages.warning(request, f'Povolený čas s ID {povoleny_cas_id} neexistuje.')
        return redirect("all_povolene_casy")
    povoleny_cas.delete()
    messages.success(request, f'Povolený čas s ID {povoleny_cas_id} bol úspešne vymazaný.')
    return redirect("all_povolene_casy")

@login_required
def all_admin_emaily(request):
    admin_emaily = AdminEmail.objects.all()
    context = {
        "admin_emaily": admin_emaily
    }
    return render(request, 'core/all_admin_emaily.html', context=context)

@login_required
def create_new_admin_email(request):
    if request.method == "GET":
        admin_email = AdminEmail.objects.all().first()
        if admin_email:
            messages.warning(request, 'Administrátorský e-mail už existuje, nemôžete vytvoriť ďalší.')
            return redirect("all_admin_emaily")
        context = {
            'form': CreateAdminEmail,
        }
        return render(request, 'core/create_new_admin_email.html', context=context)
    if request.method == "POST":
        form = CreateAdminEmail(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Úspešne ste vytvorili nový administrátorský e-mail.")
        else:
            messages.error(request, "Pri validácii dát, ktoré ste zadali, nastala chyba. Skúste to znovu.")
            context = {
                "form": form
            }
            return render(request, 'core/create_new_admin_email.html', context=context)
        return redirect("all_admin_emaily")

@login_required
def delete_admin_email(request, admin_email_id: int):
    admin_email = AdminEmail.objects.all().filter(id=admin_email_id).first()
    if not admin_email:
        messages.warning(request, f'Administrátorský e-mail s ID {admin_email_id} neexistuje.')
        return redirect("all_admin_emaily")
    admin_email.delete()
    messages.success(request, f'Administrátorský e-mail s ID {admin_email_id} bol úspešne vymazaný.')
    return redirect("all_admin_emaily")

@login_required
def all_aktivity(request):
    aktivity = Aktivita.objects.all()
    context = {
        "aktivity": aktivity
    }
    return render(request, 'core/all_aktivity.html', context=context)

@login_required
def create_new_aktivita(request):
    if request.method == "GET":
        context = {
            'form': CreateAktivitaForm,
        }
        return render(request, 'core/create_new_aktivita.html', context=context)
    if request.method == "POST":
        form = CreateAktivitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Úspešne ste vytvorili novú aktivitu.")
        else:
            messages.error(request, "Pri validácii dát, ktoré ste zadali, nastala chyba. Skúste to znovu.")
            context = {
                "form": form
            }
            return render(request, 'core/create_new_aktivita.html', context=context)
        return redirect("all_aktivity")


@login_required
def edit_aktivita(request, aktivita_id: int):
    aktivita = Aktivita.objects.all().filter(id=aktivita_id).first()
    if not aktivita:
        messages.warning(request, f'Aktivita s ID {aktivita_id} neexistuje.')
        return redirect("all_aktivity")
    if request.method == "GET":
        form = EditAktivitaForm(instance=aktivita)
        context = {
            'form': form,
            "aktivita": aktivita
        }
        return render(request, 'core/edit_aktivita.html', context=context)
    if request.method == "POST":
        form = EditAktivitaForm(data=request.POST, instance=aktivita)
        if form.is_valid():
            form.save()
            messages.success(request, "Úspešne ste zmenili aktivitu.")
        else:
            messages.error(request, "Pri validácii dát, ktoré ste zadali, nastala chyba. Skúste to znovu.")
            context = {
                "form": form,
                "aktivita": aktivita
            }
            return render(request, 'core/edit_aktivita.html', context=context)
        return redirect("all_aktivity")

@login_required
def delete_aktivita(request, aktivita_id: int):
    aktivita = Aktivita.objects.all().filter(id=aktivita_id).first()
    if not aktivita:
        messages.warning(request, f'Aktivita s ID {aktivita_id} neexistuje.')
        return redirect("all_aktivity")
    aktivita.delete()
    messages.success(request, f'Aktivita s ID {aktivita_id} bol úspešne vymazaný.')
    return redirect("all_aktivity")

@login_required
def open_or_close_system(request):
    actual_stav = Stav.objects.all().first()
    actual_stav.otvorene = not actual_stav.otvorene
    actual_stav.save()
    if actual_stav.otvorene:
        message_to_display = "Systém bol úspešne OTVORENÝ."
        send_email_notification_system_opened_to_admin()
    else:
        message_to_display = "Systém bol úspešne ZATVORENÝ."
        send_email_notification_system_closed_to_admin()
    messages.success(request, message_to_display)
    return redirect('actual_stav_systemu')

@login_required
def create_new_stav_systemu(request):
    if request.method == "GET":
        actual_stav = Stav.objects.all().first()
        if actual_stav:
            messages.warning(request, 'Stav už existuje, nemôžete vytvoriť ďalší.')
            return redirect("actual_stav_systemu")
        context = {
            'form': CreateStavForm,
        }
        return render(request, 'core/create_new_stav_systemu.html', context=context)
    if request.method == "POST":
        form = CreateStavForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Úspešne ste vytvorili nový stav systému.")
        else:
            messages.error(request, "Pri validácii dát, ktoré ste zadali, nastala chyba. Skúste to znovu.")
            context = {
                "form": form
            }
            return render(request, 'core/create_new_stav_systemu.html', context=context)
        return redirect("actual_stav_systemu")

@login_required
def actual_stav_systemu(request):
    actual_stav = Stav.objects.all().first()
    return render(request, 'core/actual_stav_systemu.html', context={"actual_stav": actual_stav})

@login_required
def create_new_nepovoleny_datum(request):
    if request.method == "GET":
        context = {
            'form': CreateNepovolenyDatumForm,
        }
        return render(request, 'core/create_new_nepovoleny_datum.html', context=context)
    if request.method == "POST":
        form = CreateNepovolenyDatumForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Úspešne ste vytvorili nový nepovolený dátum.")
        else:
            messages.error(request, "Pri validácii dát, ktoré ste zadali, nastala chyba. Skúste to znovu.")
            context = {
                "form": form
            }
            return render(request, 'core/create_new_nepovoleny_datum.html', context=context)
        return redirect("all_nepovolene_datumy")

@login_required
def all_nepovolene_datumy(request):
    nepovolene_datumy = NepovolenyDatum.objects.all().order_by('datum')
    context = {
        "nepovolene_datumy": nepovolene_datumy
    }
    return render(request, 'core/all_nepovolene_datumy.html', context=context)

@login_required
def delete_nepovoleny_datum(request, nepovoleny_datum_id: int):
    nepovoleny_datum = NepovolenyDatum.objects.all().filter(id=nepovoleny_datum_id).first()
    if not nepovoleny_datum:
        messages.warning(request, f'Nepovolený dátum s ID {nepovoleny_datum_id} neexistuje.')
        return redirect("all_nepovolene_datumy")
    nepovoleny_datum.delete()
    messages.success(request, f'Nepovolený dátum {nepovoleny_datum.datum} s ID {nepovoleny_datum_id} bol úspešne vymazaný.')
    return redirect("all_nepovolene_datumy")


@login_required
def create_new_kontaktne_cislo(request):
    if request.method == "GET":
        kontaktne_cislo = KontaktneTelefonneCislo.objects.all().first()
        if kontaktne_cislo:
            messages.warning(request, 'Kontaktné telefónne číslo už existuje, nemôžete vytvoriť ďalšie.')
            return redirect("all_kontaktne_cisla")
        context = {
            'form': CreateKontaktneTelefonneCisloForm,
        }
        return render(request, 'core/create_new_kontaktne_cislo.html', context=context)
    if request.method == "POST":
        form = CreateKontaktneTelefonneCisloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Úspešne ste vytvorili nové kontaktné telefónne číslo.")
        else:
            messages.error(request, "Pri validácii dát, ktoré ste zadali, nastala chyba. Skúste to znovu.")
            context = {
                "form": form
            }
            return render(request, 'core/create_new_kontaktne_cislo.html', context=context)
        return redirect("all_kontaktne_cisla")

@login_required
def all_kontaktne_cisla(request):
    kontaktne_cisla = KontaktneTelefonneCislo.objects.all()
    context = {
        "kontaktne_cisla": kontaktne_cisla
    }
    return render(request, 'core/all_kontaktne_cisla.html', context=context)

@login_required
def delete_kontaktne_cislo(request, kontaktne_cislo_id: int):
    kontaktne_cislo = KontaktneTelefonneCislo.objects.all().filter(id=kontaktne_cislo_id).first()
    if not kontaktne_cislo:
        messages.warning(request, f'Kontaktné telefónne číslo s ID {kontaktne_cislo_id} neexistuje.')
        return redirect("all_kontaktne_cisla")
    kontaktne_cislo.delete()
    messages.success(request, f'Kontaktné telefónne číslo {kontaktne_cislo.telefonne_cislo} s ID {kontaktne_cislo_id} bolo úspešne vymazaný.')
    return redirect("all_kontaktne_cisla")

@login_required
def create_new_nepovolena_aktivita_pre_datum(request):
    if request.method == "GET":
        # Render the form
        form = CreateNepovolenaAktivitaNaDatumForm()
        context = {
            'form': form,
        }
        return render(request, 'core/create_new_nepovolena_aktivita_pre_datum.html', context=context)
    if request.method == "POST":
        # Validate form and save it to database
        form = CreateNepovolenaAktivitaNaDatumForm(request.POST)
        if form.is_valid():
            # Check if another instance with the same data already exists
            if not NepovolenaAktivitaNaDatum.objects.filter(datum=form.cleaned_data['datum'], aktivita=form.cleaned_data["aktivita"]).exists():
                form.save()
                messages.success(request, "Úspešne ste vytvorili nový nepovolený dátum.")
            else:
                messages.warning(request, "Rovnaká nepovolená aktivita na rovnaký dátum už existuje.")
                return redirect("all_nepovolene_aktivity_pre_datumy")
        else:
            messages.error(request, "Pri validácii dát, ktoré ste zadali, nastala chyba. Skúste to znovu.")
            context = {
                "form": form
            }
            return render(request, 'core/create_new_nepovolena_aktivita_pre_datum.html', context=context)
        return redirect("all_nepovolene_aktivity_pre_datumy")


@login_required
def all_nepovolene_aktivity_pre_datumy(request):
    nepovolene_aktivity_pre_datumy = NepovolenaAktivitaNaDatum.objects.all().order_by('-datum')
    context = {
        "nepovolene_aktivity_pre_datumy": nepovolene_aktivity_pre_datumy
    }
    return render(request, 'core/all_nepovolene_aktivity_pre_datumy.html', context=context)

@login_required
def delete_nepovolena_aktivita_pre_datum(request, nepovolena_aktivita_pre_datum_id: int):
    nepovolena_aktivita_pre_datum = NepovolenaAktivitaNaDatum.objects.all().filter(id=nepovolena_aktivita_pre_datum_id).first()
    if not nepovolena_aktivita_pre_datum:
        messages.warning(request, f'Nepovolená aktivita s ID {nepovolena_aktivita_pre_datum_id} neexistuje.')
        return redirect("all_nepovolene_aktivity_pre_datumy")
    nepovolena_aktivita_pre_datum.delete()
    messages.success(request, f'Nepovolená aktivita {nepovolena_aktivita_pre_datum.aktivita.nazov} pre dátum {nepovolena_aktivita_pre_datum.datum} s ID {nepovolena_aktivita_pre_datum_id} bola úspešne vymazaná.')
    return redirect("all_nepovolene_aktivity_pre_datumy")
