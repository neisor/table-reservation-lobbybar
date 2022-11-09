from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
import uuid
from core.validators import future_date_only

class Reservation(models.Model):
    """Model for reservations"""
    class Stavy(models.TextChoices):
        """Model for holding the possible statuses of the reservations"""
        NOVA = "NOVA", "Nová"
        CAKA_SA_NA_POTVRDENIE_EMAILOVEJ_ADRESY = "CAKA_SA_NA_POTVRDENIE_EMAILOVEJ_ADRESY", "Čaká sa na potvrdenie e-mailovej adresy"
        EMAILOVA_ADRESA_POTVRDENA = "EMAILOVA_ADRESA_POTVRDENA", "E-mailová adresa potvrdená"
        SPRACOVAVA_SA = "SPRACOVAVA_SA", "Spracováva sa"
        POTVRDENA = "POTVRDENA", "Potvrdená"
        ZAMIETNUTA = "ZAMIETNUTA", "Zamietnutá"

    uuid_identificator = models.UUIDField(default=uuid.uuid4, editable=False)
    meno = models.CharField(max_length=255)
    priezvisko = models.CharField(max_length=255)
    pocet_ludi = models.PositiveIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(45)], verbose_name="Počet ľudí")
    datum = models.DateField(verbose_name="Dátum rezervácie", validators=[future_date_only])
    cas = models.TimeField(verbose_name="Čas rezervácie")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{8,15}$', message="Telefónne číslo musí byť vo formáte: '+421911222333'.")
    telefonne_cislo = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Telefónne číslo/Mobil")
    email = models.EmailField(verbose_name="E-mail")
    sprava = models.TextField(verbose_name="Správa")
    stav = models.CharField(
        max_length=40,
        choices=Stavy.choices
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Vytvorené")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Upravené")

    def __str__(self):
        return f'{self.pk} / {self.meno} {self.priezvisko} / {self.datum} {self.cas} / {self.pocet_ludi} / {self.stav}'
