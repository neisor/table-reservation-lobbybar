from django.core.management import BaseCommand, CommandError
from django.contrib.auth.models import User

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
