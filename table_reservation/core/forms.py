from django.forms import ModelForm
from django import forms
from core.models import PovolenyCas, AdminEmail, Aktivita, Stav, NepovolenyDatum, KontaktneTelefonneCislo

class CreatePovolenyCasForm(ModelForm):
    class Meta:
        model = PovolenyCas
        fields = "__all__"
        widgets = {
            'cas_rezervacii_od': forms.TimeInput(format=('%H:%M'), attrs={'class':'form-control', 'placeholder':'Vyberte čas rezervácií od', 'type':'time'}),
            'cas_rezervacii_do': forms.TimeInput(format=('%H:%M'), attrs={'class':'form-control', 'placeholder':'Vyberte čas rezervácií do', 'type':'time'}),
        }

class EditPovolenyCasForm(CreatePovolenyCasForm):
    pass

class CreateAdminEmail(ModelForm):
    class Meta:
        model = AdminEmail
        fields = "__all__"
    
class CreateAktivitaForm(ModelForm):
    class Meta:
        model = Aktivita
        fields = "__all__"

class EditAktivitaForm(CreateAktivitaForm):
    pass

class CreateStavForm(ModelForm):
    class Meta:
        model = Stav
        fields = "__all__"

class CreateNepovolenyDatumForm(ModelForm):
    class Meta:
        model = NepovolenyDatum
        fields = "__all__"
        widgets = {
            'datum': forms.DateInput(format=('%d.%m.%Y'), attrs={'class':'form-control', 'placeholder':'Vyberte nepovolený dátum', 'type':'date'}),
        }

class CreateKontaktneTelefonneCisloForm(ModelForm):
    class Meta:
        model = KontaktneTelefonneCislo
        fields = "__all__"
