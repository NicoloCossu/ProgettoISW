from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Animale(models.Model):
    ID_animale = models.AutoField(primary_key=True)
    specie = models.CharField(max_length=100)
    razza = models.CharField(max_length=50)
    età = models.IntegerField(default=0)
    descrizione = models.CharField(max_length=400)

    #resistuisce l'ID dell'animale
    def __str__(self):
        return str(self.ID_animale)

class RichiestaAdozione(models.Model):
    ID_richiestaAdozione = models.AutoField(primary_key=True)
    utente = models.ForeignKey(User, on_delete=models.PROTECT, null=True, default=0)
    animale = models.ForeignKey(Animale, on_delete=models.CASCADE, null=True, default=1)
    nomeCognome = models.CharField(max_length=320)
    indirizzo = models.CharField(max_length= 400)
    emailNumeroDiTelefono = models.CharField(max_length= 500)
    richiesta = models.CharField(max_length= 400, null=False, default="in attesa")

    #restituisce l'id della richiesta di adozione con il nome e il cognome del utente
    def __str__(self):
        return f"Richiesta di adozione {self.ID_richiestaAdozione}: {self.nomeCognome}"

    
    

