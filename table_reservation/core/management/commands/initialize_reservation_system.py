from django.core.management import BaseCommand
from django.contrib.auth.models import User
from core.models import PovolenyCas, AdminEmail, Aktivita, Stav
import datetime

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.password = 'admin'
        self.stdout.write(f'Creating initial admin user with password: {self.password}')
        if User.objects.all().filter(username='admin'):
            self.stdout.write('User with username admin already exists! Not creating a new one.')
        else:
            user = User.objects.create_user('admin', 'change-me@change-me.com', self.password)
            user.is_staff = True
            user.is_superuser = True
            user.is_admin = True
            user.save()
            self.stdout.write('User successfully created!')

        self.stdout.write('\nCreating PovolenyCas...')
        if PovolenyCas.objects.exists():
            self.stdout.write('PovolenyCas already exists! Not creating a new one.')
        else:
            povoleny_cas = PovolenyCas.objects.create(
                cas_rezervacii_od=datetime.time(hour=15, minute=00),
                cas_rezervacii_do=datetime.time(hour=21, minute=30),
            )
            povoleny_cas.save()
            self.stdout.write('PovolenyCas successfully created!')

        self.stdout.write('\nCreating AdminEmail')
        if AdminEmail.objects.exists():
            self.stdout.write('AdminEmail already exists! Not creating a new one.')
        else:
            admin_email = AdminEmail.objects.create(email="change-me@change-me.com")
            admin_email.save()
            self.stdout.write('AdminEmail successfully created!')

        self.stdout.write('\nCreating Aktivita')
        if Aktivita.objects.exists():
            self.stdout.write('At least 1 Aktivita already exists! Not creating a new one.')
        else:
            aktivita = Aktivita.objects.create(nazov="JEDLO")
            aktivita.save()
            self.stdout.write('Aktivita successfully created!')

        self.stdout.write('\nCreating Stav')
        if Stav.objects.exists():
            self.stdout.write('At least 1 Stav already exists! Not creating a new one.')
        else:
            stav = Stav.objects.create(otvorene=True)
            stav.save()
            self.stdout.write('Stav successfully created!')

        self.stdout.write('\nDONE!')
