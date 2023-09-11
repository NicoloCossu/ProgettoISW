from django.test import TestCase
from .models import Animale, RichiestaAdozione, Utente

#test unitario per la classe Animale fa un controllo sulla lunghezza dei campi che deve essere maggiore di 0, non possiamo inserire una
#stringa vuota quando viene inserito nel db e viene fatto un controllo anche sulla lunghezza massima definita nei models.
class AnimaleTestCase(TestCase):
    def setUp(self):
        Animale.objects.create(razza="Cane", specie="a", età=3, descrizione="Un simpatico cane")
    def test_lunghezzaCampi(self):
            animale = Animale.objects.get()
            self.assertEqual(len(animale.specie) > 0,  True)
            self.assertEqual(len(animale.specie) <=100,  True)
            self.assertEqual(len(animale.razza) > 0,  True)
            self.assertEqual(len(animale.razza) <= 50,  True)
            self.assertEqual(animale.età > 0,  True)
            self.assertEqual(len(animale.descrizione) > 0,  True)
            self.assertEqual(len(animale.descrizione) <= 400,  True)

class AnimaleCorrettoTestCase(TestCase):
    def setUp(self):
        self.animale = Animale.objects.create(razza="Cane", specie="a", età=3, descrizione="Un simpatico cane")
    def test_lunghezzaCampi(self):
        self.assertTrue(len(self.animale.specie) > 0, "Il campo specie dovrebbe avere una lunghezza maggiore di 0")


#test unitario per la classe RichiestaAdozione permette un controllo sulla lunghezza dei campi imponendo una lunghezza minima e una massima
class RichiestaAdozioneTestCase(TestCase):
    def setUp(self):
        RichiestaAdozione.objects.create(nomeCognome="Mario Rossi", indirizzo="Via Roma 10, Cagliari", emailNumeroDiTelefono="ClaudioCrobu69@gmail.com")

    def test_lunghezzaCampi(self):
        richiestaAdozione = RichiestaAdozione.objects.get()
        self.assertEqual(len(richiestaAdozione.nomeCognome) > 0,  True)
        self.assertEqual(len(richiestaAdozione.nomeCognome) <= 320,  True)
        self.assertEqual(len(richiestaAdozione.indirizzo) > 0,  True)
        self.assertEqual(len(richiestaAdozione.indirizzo) < 400,  True)
        self.assertEqual(len(richiestaAdozione.emailNumeroDiTelefono) > 0,  True)
        self.assertEqual(len(richiestaAdozione.emailNumeroDiTelefono) <= 500,  True)
     
# Create your tests here.
#class Utente(models.Model):
  #  nome = models.CharField(max_length=100)
  #  cognome = models.CharField(max_length=100)
  #  età = models.IntegerField(default=18)
  #  email = models.CharField(max_length=400)
   # password = models.CharField(max_length=30)

class UtenteTestCase(TestCase):
    def setUp(self):
        Utente.objects.create(nome="Nicolo", cognome="Cossu", età=2, email="test@tiscali.it",password="")

    def testUtenteCorretto(self):
        utenteCorretto = Utente.objects.get()
        self.assertEqual(len(utenteCorretto.nome) >0, True)
        self.assertEqual(len(utenteCorretto.nome) <100, True)
        self.assertEqual(len(utenteCorretto.cognome) >0, True)
        self.assertEqual(len(utenteCorretto.cognome) <=100, True)
        self.assertEqual(utenteCorretto.età>0, True)