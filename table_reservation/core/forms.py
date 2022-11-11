from django.forms import ModelForm
from django import forms
from core.models import PovolenyCas, AdminEmail

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
    