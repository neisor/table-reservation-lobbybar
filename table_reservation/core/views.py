from django.shortcuts import render, redirect
from core.forms import CreatePovolenyCasForm, EditPovolenyCasForm
from core.models import PovolenyCas
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
