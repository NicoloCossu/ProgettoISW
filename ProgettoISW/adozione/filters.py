import django_filters

from .models import *

class AnimalFilter(django_filters.FilterSet):
    class Meta:
        model = Animale
        fields = '__all__'

class RichesteFilter(django_filters.FilterSet):
    class Meta:
        model = RichiestaAdozione
        fields = ['nomeCognome', 'indirizzo', 'emailNumeroDiTelefono', 'animale']
