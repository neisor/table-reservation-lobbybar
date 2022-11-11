from django.forms import ModelForm, ValidationError
from django import forms
from core.models import Reservation, PovolenyCas
import datetime
from captcha.fields import ReCaptchaField

class CreateReservationForm(ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Reservation
        exclude = ('uuid_identificator', 'stav')
        widgets = {
            'datum': forms.DateInput(format=('%d.%m.%Y'), attrs={'class':'form-control', 'placeholder':'Vyberte dátum', 'type':'date'}),
            'cas': forms.TimeInput(format=('%H:%M'), attrs={'class':'form-control', 'placeholder':'Vyberte čas', 'type':'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        datum = cleaned_data.get("datum")
        cas = cleaned_data.get("cas")
        datum_a_cas_z_formulara = datetime.datetime.combine(datum, cas)
        now_plus_2_hours = datetime.datetime.now() + datetime.timedelta(hours=2)
        povoleny_cas = PovolenyCas.objects.all().first()
        if not povoleny_cas:
            raise ValidationError('Nie je možné zvalidovať čas rezervácie. Je potrebné pridať povolené časy.')
        cas_rezervacii_od = povoleny_cas.cas_rezervacii_od
        cas_rezervacii_do = povoleny_cas.cas_rezervacii_do
        if datum_a_cas_z_formulara < now_plus_2_hours:
            raise ValidationError('Dátum a čas nemôže byť v minulosti a menej ako 2 hodiny pred požadovanou rezerváciou.')
        if cas > cas_rezervacii_do or cas < cas_rezervacii_od:
            raise ValidationError('Čas rezervácie musí byť medzi 15:00 až 20:30.')
        