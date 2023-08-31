from django import forms
from .models import RichiestaAdozione

class RichiestaAdozioneForm(forms.ModelForm):
    class Meta:
        model = RichiestaAdozione
        fields = ['nomeCognome', 'indirizzo', 'emailNumeroDiTelefono']
