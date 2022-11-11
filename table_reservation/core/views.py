from django.shortcuts import render, redirect
from core.forms import *
from core.models import PovolenyCas, AdminEmail, Aktivita
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
        povoleny_cas = AdminEmail.objects.all().first()
        if povoleny_cas:
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
