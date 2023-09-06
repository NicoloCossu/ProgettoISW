from django import forms
from .models import RichiestaAdozione

class RichiestaAdozioneForm(forms.ModelForm):
    class Meta:
        model = RichiestaAdozione
        fields = ['nomeCognome', 'indirizzo', 'emailNumeroDiTelefono']
        labels = {
            'nomeCognome': 'Nome e Cognome',
            'indirizzo': 'Indirizzo',
            'emailNumeroDiTelefono': 'Email o Numero di Telefono',
        }
