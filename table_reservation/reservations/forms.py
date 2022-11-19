from django.forms import ModelForm, ValidationError
from django import forms
from core.models import Reservation, PovolenyCas
import datetime
from django.utils.safestring import mark_safe

class CreateReservationForm(ModelForm):
    privacy_policy = forms.BooleanField()
    class Meta:
        model = Reservation
        exclude = ('uuid_identificator', 'stav', 'poznamka_administratora')
        widgets = {
            'datum': forms.DateInput(format=('%d.%m.%Y'), attrs={'class':'form-control', 'placeholder':'Vyberte dátum', 'type':'date'}),
            'cas': forms.TimeInput(format=('%H:%M'), attrs={'class':'form-control', 'placeholder':'Vyberte čas', 'type':'time'}),
            'aktivita': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(CreateReservationForm, self).__init__(*args, **kwargs)
        self.fields['aktivita'].label = 'Ako plánujete stráviť večer u nás?'
        self.fields['privacy_policy'].label = mark_safe(
            'Súhlasím so <a href="https://elnacional.sk/ochrana-osobnych-udajov">spracovaním osobných údajov</a>'
        )

    def clean(self):
        cleaned_data = super().clean()
        datum = cleaned_data.get("datum")
        cas = cleaned_data.get("cas")
        if type(datum) != datetime.date:
            raise ValidationError('Dátum rezervácie ste nezadali v správnom formáte.')  # Needed in case when user does not use date-picker
        if type(cas) != datetime.time:
            raise ValidationError('Čas rezervácie ste nezadali v správnom formáte.')  # Needed in case when user does not use time-picker
        datum_a_cas_z_formulara = datetime.datetime.combine(datum, cas)
        now_plus_2_hours = datetime.datetime.now() + datetime.timedelta(hours=2)  # Do not allow for a reservation sooner than 2 hours from now
        # Get casy from PovolenyCas model
        povoleny_cas = PovolenyCas.objects.all().first()
        cas_rezervacii_od = povoleny_cas.cas_rezervacii_od
        cas_rezervacii_do = povoleny_cas.cas_rezervacii_do
        # Perform validations
        if not povoleny_cas:
            raise ValidationError('Nie je možné zvalidovať čas rezervácie. Je potrebné pridať povolené časy.')
        if datum_a_cas_z_formulara < now_plus_2_hours:
            raise ValidationError('Dátum a čas nemôže byť v minulosti a menej ako 2 hodiny pred požadovanou rezerváciou.')
        if cas > cas_rezervacii_do or cas < cas_rezervacii_od:
            raise ValidationError(f'Čas rezervácie musí byť medzi {cas_rezervacii_od.strftime("%H:%M")} až {cas_rezervacii_do.strftime("%H:%M")}.')
        
class EditPoznamkaAdministratora(ModelForm):
    class Meta:
        model = Reservation
        fields = ['poznamka_administratora']
