from django.contrib import admin
from core.models import Reservation, Aktivita, AdminEmail, PovolenyCas, Stav

# Register your models here.
admin.site.register(Reservation)
admin.site.register(Aktivita)
admin.site.register(AdminEmail)
admin.site.register(PovolenyCas)
admin.site.register(Stav)