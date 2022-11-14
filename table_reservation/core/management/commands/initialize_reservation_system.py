from django.core.management import BaseCommand, CommandError
from django.contrib.auth.models import User
from core.models import PovolenyCas, AdminEmail, Aktivita
import datetime

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.password = 'admin'
        self.stdout.write(f'Creating initial admin user with password: {self.password}')
        user = User.objects.create_user('admin', 'change-me@change-me.com', self.password)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save()
        self.stdout.write('User successfully created!')

        self.stdout.write('Creating PovolenyCas...')
        povoleny_cas = PovolenyCas.objects.create(
            cas_rezervacii_od=datetime.time(hour=15, minute=00),
            cas_rezervacii_do=datetime.time(hour=21, minute=30),
        )
        povoleny_cas.save()

        self.stdout.write('Creating AdminEmail')
        admin_email = AdminEmail.objects.create(email="change-me@change-me.com")
        admin_email.save()

        self.stdout.write('Creating Aktivita')
        aktivita = Aktivita.objects.create(nazov="JEDLO")
        aktivita.save()

        self.stdout.write('DONE!')
