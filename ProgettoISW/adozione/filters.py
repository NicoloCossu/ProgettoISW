import django_filters

from .models import *

#Filtro per la ricerca degli animali 
class AnimalFilter(django_filters.FilterSet):
    class Meta:
        model = Animale
        fields = '__all__'
#Filtro per la ricerca delle richieste di adozione per nomeCognome, indirizzo, emailNumerodiTelefono e animale
class RichesteFilter(django_filters.FilterSet):
    class Meta:
        model = RichiestaAdozione
        fields = ['nomeCognome', 'indirizzo', 'emailNumeroDiTelefono', 'animale']
