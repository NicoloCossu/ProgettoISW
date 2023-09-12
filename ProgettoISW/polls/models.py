from django.db import models

# Create your models here.
class Animale(models.Model):
    specie = models.CharField(max_length=100)
    razza = models.CharField(max_length=50)
    età = models.IntegerField(default=0)
    descrizione = models.CharField(max_length=400)

class Utente(models.Model):
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    età = models.IntegerField(default=18)
    email = models.CharField(max_length=400)
    password = models.CharField(max_length=30)

class RichiestaAdozione(models.Model):
    nomeCognome = models.CharField(max_length=320)
    indirizzo = models.CharField(max_length= 400)
    emailNumeroDiTelefono = models.CharField(max_length= 500)

