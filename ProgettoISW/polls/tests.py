from django.test import TestCase
from .models import Animale, RichiestaAdozione

class AnimaleTestCase(TestCase):
    def setUp(self):
        Animale.objects.create(razza="Cane", specie="a", età=3, descrizione="Un simpatico cane")

    def test_lunghezzaCampi(self):
        animale = Animale.objects.get()
        self.assertEqual(len(animale.specie) > 0,  True)
        self.assertEqual(len(animale.razza) > 0,  True)
        self.assertEqual(animale.età > 0,  True)
        self.assertEqual(len(animale.descrizione) > 0,  True)

class RichiestaAdozioneTestCase(TestCase):
      

    def setUp(self):
        RichiestaAdozione.objects.create(nomeCognome="Mario Rossi", indirizzo="Via Roma 10, Cagliari", emailNumeroDiTelefono="ClaudioCrobu69@gmail.com")

    def test_lunghezzaCampi(self):
        richiestaAdozione = RichiestaAdozione.objects.get()
        self.assertEqual(len(richiestaAdozione.nomeCognome) > 0,  True)
        self.assertEqual(len(richiestaAdozione.indirizzo) > 0,  True)
        self.assertEqual(len(richiestaAdozione.emailNumeroDiTelefono) > 0,  True)
     
# Create your tests here.
