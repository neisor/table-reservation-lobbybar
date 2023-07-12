from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.forms import ValidationError
import uuid
from core.validators import future_date_only

class Reservation(models.Model):
    """Model for reservations"""
    class Stavy(models.TextChoices):
        """Model for holding the possible statuses of the reservations"""
        NOVA = "NOVA", "Nová"
        CAKA_SA_NA_POTVRDENIE_EMAILOVEJ_ADRESY = "CAKA_SA_NA_POTVRDENIE_EMAILOVEJ_ADRESY", "Čaká sa na potvrdenie e-mailovej adresy"
        EMAILOVA_ADRESA_POTVRDENA = "EMAILOVA_ADRESA_POTVRDENA", "E-mailová adresa potvrdená"
        PRIJATA = "PRIJATA", "Prijatá"
        ZAMIETNUTA = "ZAMIETNUTA", "Zamietnutá"

    uuid_identificator = models.UUIDField(default=uuid.uuid4)
    meno = models.CharField(max_length=255)
    priezvisko = models.CharField(max_length=255)
    pocet_ludi = models.PositiveIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(45)], verbose_name="Počet ľudí")
    datum = models.DateField(verbose_name="Dátum rezervácie", validators=[future_date_only])
    cas = models.TimeField(verbose_name="Čas rezervácie")
    aktivita = models.ManyToManyField(to='Aktivita')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{8,15}$', message="Telefónne číslo vo formáte: '+421911222333'.")
    telefonne_cislo = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Telefónne číslo/Mobil")
    email = models.EmailField(verbose_name="E-mail")
    sprava = models.TextField(verbose_name="Správa", null=True, blank=True)
    stav = models.CharField(
        max_length=40,
        choices=Stavy.choices
    )
    poznamka_administratora = models.TextField(verbose_name="Poznámka administrátora", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Vytvorené")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Upravené")

    def __str__(self):
        return f'{self.pk} / {self.meno} {self.priezvisko} / {self.datum} {self.cas} / {self.pocet_ludi} / {self.stav}'

class Aktivita(models.Model):
    nazov = models.CharField(max_length=100, verbose_name="Názov")

    def __str__(self):
        return f'{self.nazov}'

class PovolenyCas(models.Model):
    cas_rezervacii_od = models.TimeField(verbose_name="Povolený čas rezervácií od")
    cas_rezervacii_do = models.TimeField(verbose_name="Povolený čas rezervácií do")

    def __str__(self):
        return f'Čas od {self.cas_rezervacii_od} do {self.cas_rezervacii_do}'

    def save(self, *args, **kwargs):
        # if we will not check for self.pk 
        # then error will also get raised in update of existing model
        if not self.pk and PovolenyCas.objects.exists():
            raise ValidationError('Môže existovať iba jedna inštancia povolených časov.')
        return super(PovolenyCas, self).save(*args, **kwargs)

class AdminEmail(models.Model):
    email = models.EmailField(verbose_name="Administrátorský e-mail")

    def __str__(self):
        return f'E-mail: {self.email}'

    def save(self, *args, **kwargs):
        # if we will not check for self.pk 
        # then error will also get raised in update of existing model
        if not self.pk and AdminEmail.objects.exists():
            raise ValidationError('Môže existovať iba jedna inštancia administrátorského e-mailu.')
        return super(AdminEmail, self).save(*args, **kwargs)

class Stav(models.Model):
    otvorene = models.BooleanField(default=True)

    def __str__(self):
        return "Otvorené" if self.otvorene else "Zatvorené"

    def save(self, *args, **kwargs):
        # if we will not check for self.pk 
        # then error will also get raised in update of existing model
        if not self.pk and Stav.objects.exists():
            raise ValidationError('Môže existovať iba jedna inštancia stavu.')
        return super(Stav, self).save(*args, **kwargs)

class NepovolenyDatum(models.Model):
    """Model for defining not allowed dates for reservations"""
    datum = models.DateField(verbose_name="Nepovolený dátum")

    def __str__(self):
        return f"Nepovolený dátum: {self.datum}"
    
    def save(self, *args, **kwargs):
        """Make sure to allow only 1 instance for 1 date"""
        if NepovolenyDatum.objects.all().filter(datum=self.datum):
            raise ValidationError("Môže existovať iba jeden záznam nepovoleného dátumu pre konkrétny dátum.")
        return super(NepovolenyDatum, self).save(*args, **kwargs)

class KontaktneTelefonneCislo(models.Model):
    """Model for defining a contact number"""
    phone_regex = RegexValidator(regex=r'^\+?1?\d{8,15}$', message="Telefónne číslo vo formáte: '+421911222333'.")
    telefonne_cislo = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Telefónne číslo/Mobil")

    def __str__(self):
        return f"Kontaktné tel. č.: {self.telefonne_cislo}"

    def save(self, *args, **kwargs):
        # if we will not check for self.pk 
        # then error will also get raised in update of existing model
        if not self.pk and KontaktneTelefonneCislo.objects.exists():
            raise ValidationError('Môže existovať iba jedna inštancia kontaktného telefónneho čísla.')
        return super(KontaktneTelefonneCislo, self).save(*args, **kwargs)

class NepovolenaAktivitaNaDatum(models.Model):
    aktivita = models.ForeignKey(to='Aktivita', on_delete=models.CASCADE, verbose_name="Nepovolená aktivita")
    datum = models.DateField(verbose_name="Dátum pre nepovolenú aktivitu")

    def __str__(self):
        return f"Nepovolená aktivita: {self.aktivita.nazov} / Dátum: {self.datum}"
    