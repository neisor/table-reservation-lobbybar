from django.forms import ModelForm, ValidationError
from django import forms
from core.models import Reservation, PovolenyCas, KontaktneTelefonneCislo
import datetime
from django.utils.safestring import mark_safe
from reservations.helpers import get_available_aktivity_for_a_date

class DateInputForReservationForm(forms.Form):
    datum = forms.DateField(widget=forms.DateInput(format=('%d.%m.%Y'), attrs={'class':'form-control', 'placeholder':'Vyberte dátum', 'type':'date'}))
    widgets = {
        'datum': forms.DateInput(format=('%d.%m.%Y'), attrs={'class':'form-control', 'placeholder':'Vyberte dátum', 'type':'date'}),
    }
    def __init__(self, *args, **kwargs):
        super(DateInputForReservationForm, self).__init__(*args, **kwargs)
        self.fields['datum'].label = 'Vyberte si dátum rezervácie'

class CreateReservationForm(ModelForm):
    privacy_policy = forms.BooleanField()
    class Meta:
        model = Reservation
        exclude = ('uuid_identificator', 'stav', 'poznamka_administratora')
        widgets = {
            'cas': forms.TimeInput(format=('%H:%M'), attrs={'class':'form-control', 'placeholder':'Vyberte čas', 'type':'time'}),
            'aktivita': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        # datum variable will either be a datetime.date type when being rendered for the user to input, or, a string after the form is submitted and is being validated 
        datum = kwargs.pop('datum') if kwargs.get('datum') else None  
        super(CreateReservationForm, self).__init__(*args, **kwargs)
        self.fields['aktivita'].label = 'Ako si želáte stráviť čas u nás?'
        self.fields['privacy_policy'].label = mark_safe(
            'Súhlasím so <a href="https://lobbybar.sk/ochrana-osobnych-udajov">spracovaním osobných údajov</a>'
        )
        if datum:
            # Show only available Aktivity options for the selected date (Aktivity which are not in NepovolenaAktivitaNaDatum)
            allowed_activities_for_today = get_available_aktivity_for_a_date(date=datum)
            if not allowed_activities_for_today:
                kontaktne_tel_cislo = KontaktneTelefonneCislo.objects.all().first()
                self.fields["aktivita"].help_text = f"""
                <b>Aktuálne nie sú k dispozícii žiadne možnosti ako stráviť večer u nás pre tento konkrétny dátum.</b><br/>
                Pre viac informácií kontaktujte prevádzkara/ku na tel. č.: <a href="tel:{kontaktne_tel_cislo.telefonne_cislo if kontaktne_tel_cislo else ''}">{kontaktne_tel_cislo.telefonne_cislo if kontaktne_tel_cislo else ''}</a>
                """
            self.fields["aktivita"].queryset = allowed_activities_for_today
            self.fields["datum"].initial = datetime.datetime.strftime(datum, '%d.%m.%Y') if not isinstance(datum, str) else datum
            self.fields["datum"].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        datum = cleaned_data.get("datum")
        cas = cleaned_data.get("cas")
        if type(datum) != datetime.date:
            raise ValidationError('Dátum rezervácie ste nezadali v správnom formáte.')  # Needed in case when user does not use date-picker
        if type(cas) != datetime.time:
            raise ValidationError('Čas rezervácie ste nezadali v správnom formáte.')  # Needed in case when user does not use time-picker
        datum_a_cas_z_formulara = datetime.datetime.combine(datum, cas)
        now_plus_hours = datetime.datetime.now() + datetime.timedelta(hours=4)  # Do not allow for a reservation sooner than 2 hours from now
        # Get casy from PovolenyCas model
        povoleny_cas = PovolenyCas.objects.all().first()
        cas_rezervacii_od = povoleny_cas.cas_rezervacii_od
        cas_rezervacii_do = povoleny_cas.cas_rezervacii_do
        # Perform validations
        if not povoleny_cas:
            raise ValidationError('Nie je možné zvalidovať čas rezervácie. Je potrebné pridať povolené časy.')
        if datum_a_cas_z_formulara < now_plus_hours:
            raise ValidationError('Dátum a čas ktorý ste zvolili nemôže byť v minulosti a taktiež ani menej ako 4 hodiny pred požadovanou rezerváciou.')
        if cas > cas_rezervacii_do or cas < cas_rezervacii_od:
            raise ValidationError(f'Čas rezervácie musí byť medzi {cas_rezervacii_od.strftime("%H:%M")} až {cas_rezervacii_do.strftime("%H:%M")}.')
        
class EditPoznamkaAdministratora(ModelForm):
    class Meta:
        model = Reservation
        fields = ['poznamka_administratora']

class FilterReservationsByDateForm(forms.Form):
    datum = forms.DateField(
        widget=forms.DateInput(
            format=('%d.%m.%Y'), attrs={'class':'form-control', 'placeholder':'Vyberte dátum', 'type':'date'}
        )
    )
