from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from accounts.forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib import messages

def login_user(request):
    if request.user.is_authenticated:
        messages.info(request, "Už ste prihlásený do systému.")
        return redirect("create_new_reservation")
    if request.method == "GET":
        context = {"form": CustomAuthenticationForm}
        return render(request, "accounts/login.html", context=context)
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Boli ste úspešne prihlásený do objednávkového systému.")
                return redirect('create_new_reservation')
            else:
                messages.error(request, "Neplatné prihlasovacie údaje. Skúste to znova.")
                return redirect('login')
        else:
            messages.error(request, "Pri validácii dát, ktoré ste zadali, nastala chyba. Skúste to znovu.")
            return redirect('login')

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Boli ste úspešne odhlásený zo systému.")
        return redirect("create_new_reservation")
    else:
        messages.info(request, "Nie ste prihlásený do systému.")
        return redirect("create_new_reservation")

# def register_user(request):
#     if request.user.is_authenticated:
#         messages.info(request, "Zaregistrovať sa môžu len používatelia, ktorí nie sú prihlásený do systému.")
#         return redirect("create_new_reservation")
#     if request.method == "GET":
#         context = {"form": CustomUserCreationForm}
#         return render(request, "accounts/register.html", context=context)
#     if request.method == "POST":
#         form = CustomUserCreationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Boli ste úspešne zaregistrovaný do objednávkového systému. Teraz sa môžete prihlásiť.")
#             return redirect('login')
#         else:
#             messages.error(request, "Pri kontrole dát, ktoré ste zadali, nastala chyba. Dáta musia spĺňať popísané kritéria. Skúste to znovu.")
#             return redirect('register')