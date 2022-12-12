from core.models import Stav
from django.contrib import messages
from django.shortcuts import render

def allow_only_if_is_open(func):
    '''Decorator that checks if the table reservation system is in a Stav open or closed.'''
    def wrap(*args, **kwargs):
        request = args[0]
        is_open = Stav.objects.all().first()
        if not is_open:  # If object does not exist
            messages.warning(request, 'Aktuálne nie je možné vytvárať nové rezervácie. Administrátor musí najprv vytvoriť prvotný Stav.')
            if not request.user.is_authenticated: # Render the closed_system.html template only if user is not logged in
                return render(request, 'core/closed_system.html')
        else:
            if not is_open.otvorene:  # If otvorene is False (meaning it is zatvorene)
                messages.warning(request, 'Aktuálne nie je možné vytvárať nové rezervácie. Skúste to neskôr, prosím.')
                if not request.user.is_authenticated: # Render the closed_system.html template only if user is not logged in
                    return render(request, 'core/closed_system.html')
        result = func(*args, **kwargs)
        return result
    return wrap
