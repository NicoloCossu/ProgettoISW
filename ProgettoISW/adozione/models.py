from django.db import models

# Create your models here.
class Animale(models.Model):
    ID_animale = models.CharField(max_length=30, default="Animale", primary_key=True)
    specie = models.CharField(max_length=100)
    razza = models.CharField(max_length=50)
    età = models.IntegerField(default=0)
    descrizione = models.CharField(max_length=400)

    #resistuisce l'ID dell'animale
    def __str__(self):
        return self.ID_animale

class Utente(models.Model):
    nome = models.CharField(max_length=100, default="")
    cognome = models.CharField(max_length=100, default= "")
    età = models.IntegerField(default=18)
    email = models.CharField(max_length=400, default="a@email.it")
    password = models.CharField(max_length=30, default="Password")
    confermaPassword = models.CharField(max_length=30, default="Password")
    #restituisce nome e cognome dell'utente
    def __str__(self):
        return self.nome + self.cognome

class RichiestaAdozione(models.Model):
    ID_richiestaAdozione = models.CharField(max_length=30, default=0, primary_key=True)

    utente = models.ForeignKey(Utente, on_delete=models.PROTECT, null=True, default=0)
    animale = models.ForeignKey(Animale, on_delete=models.PROTECT, null=True, default="Animale")
    nomeCognome = models.CharField(max_length=320)
    indirizzo = models.CharField(max_length= 400)
    emailNumeroDiTelefono = models.CharField(max_length= 500)
    #restituisce l'id della richiesta di adozione
    def __str__(self):
        return self.ID_richiestaAdozione
    
