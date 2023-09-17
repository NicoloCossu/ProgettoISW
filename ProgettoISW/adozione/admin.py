from django.contrib import admin

from .models import Animale, Utente, RichiestaAdozione

# Register your models here.
admin.site.register(Animale)
admin.site.register(Utente)
admin.site.register(RichiestaAdozione)
