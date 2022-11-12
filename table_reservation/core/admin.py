from django.contrib import admin
from core.models import Reservation, Aktivita, AdminEmail

# Register your models here.
admin.site.register(Reservation)
admin.site.register(Aktivita)
admin.site.register(AdminEmail)