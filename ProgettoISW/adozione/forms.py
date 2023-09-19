from django import forms
from .models import RichiestaAdozione, Animale
from django.contrib.auth.models import User

from django.forms.widgets import HiddenInput  # Importa il widget HiddenInput

class RichiestaAdozioneForm(forms.ModelForm):
    class Meta:
        model = RichiestaAdozione
        fields = ['nomeCognome', 'indirizzo', 'emailNumeroDiTelefono', 'animale', 'utente']
        labels = {
            'nomeCognome': 'Nome e Cognome',
            'indirizzo': 'Indirizzo',
            'emailNumeroDiTelefono': 'Email o Numero di Telefono',
        }
    
    animale = forms.ModelChoiceField(queryset=Animale.objects.all(), widget=HiddenInput())
    utente = forms.ModelChoiceField(queryset=User.objects.all(), widget=HiddenInput())
    def save(self, commit =True):
        richiesta_adozione = super(RichiestaAdozioneForm, self).save(commit=False)
        richiesta_adozione.nomeCognome = self.cleaned_data['nomeCognome']
        richiesta_adozione.indirizzo = self.cleaned_data['indirizzo']
        richiesta_adozione.emailNumeroDiTelefono = self.cleaned_data['emailNumeroDiTelefono']
        if commit:
            richiesta_adozione.save()
        return richiesta_adozione 