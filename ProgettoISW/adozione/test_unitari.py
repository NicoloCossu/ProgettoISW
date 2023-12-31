from django.test import TestCase
from .models import Animale, RichiestaAdozione
from django.contrib.auth.models import User
from django.urls import reverse
from adozione.filters import AnimalFilter, RichesteFilter
from django.contrib.auth import login, logout

class LogoutViewTestCase(TestCase):
    def setUp(self):
        # Crea un utente di prova per il test
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
    #test per il logout effettua il login e simula il click del tasto LOGOUT
    def test_logout_view(self):
            self.client.login(username='testuser', password='testpassword')
            response = self.client.get(reverse('logout'))
            self.assertFalse(response.wsgi_request.user.is_authenticated)

#Test per l'accesso di un utente normale e Admin verifica che i due utenti siano reindirizzati alla pagina corretta
class UserOrSuperUserAdmin(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.superuser = User.objects.create_superuser(
            username='superuser',
            password='superuserpassword',
            email='superuser@example.com'
        )
    def test_home_view_superuser(self):
            # Effettua l'accesso come superuser 
            self.client.login(username='superuser', password='superuserpassword')
            response = self.client.get(reverse('home_amministratore'))
            self.assertEqual(response.status_code, 200)

    def test_home_view_regular_user(self):
            # Effettua l'accesso come utente normale 
            self.client.logout()
            self.client.login(username='testuser', password='testpassword')
            response = self.client.get(reverse('home'))
            self.assertEqual(response.status_code, 200)

#Test per l'inserimento di un nuovo animale 
class AnimaleTestCase(TestCase):
    #Crea un animale in modo corretto e viene inserito nel database, abbiamo simulato il passaggio di dati
    #alla pagina come nel form di inserimento dei dati
    def test_crea_animale(self):
            data = {
                'ID_animale' : '2',
                'specie' : 'Cane',
                'razza' : 'Labrador',
                'età' : 12,
                'descrizione' : 'Buono'
            }
            url = reverse('aggiungiAnimale')

            response = self.client.post(url,data)

            self.assertRedirects(response, reverse('lista_animaliAmministratore'), status_code=302)

            self.assertTrue(Animale.objects.filter(età = 12, razza = 'Labrador').exists())
    #Crea un animale in modo non orretto il test passa e non viene inserito nel database
    def testCreaAnimaleSbagliato(self):
            data = {
                'ID_animale' : '2',
                'specie' : 'Cane',
                'razza' : 'Labrajaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaador',
                'età' : 22,
                'descrizione' : 'Buono'
            }
            url = reverse('aggiungiAnimale')    
            #il test deve passare perche la razza ha più di 50 caratteri
            self.assertFalse(Animale.objects.filter(età = 22).exists())

class AdottaViewTestCase(TestCase):
    def setUp(self):
        # Crea un utente di esempio e un animale di esempio
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.animale = Animale.objects.create(ID_animale = 1, specie='Gatto', razza='GattoBlu', età=12, descrizione="Carino")

    def test_adotta_view(self):
        # Effettua l'accesso come l'utente di esempio
        self.client.login(username='testuser', password='testpassword')

        url = reverse('adotta', args=[self.animale.ID_animale])

        # Simula una richiesta POST al link 'adotta' con i dati del form
        response = self.client.post(url, {
            'nomeCognome': 'Nome Cognome', 
            'indirizzo': 'Indirizzo',  
            'emailNumeroDiTelefono': 'email@example.com',  
            'azione': 'in attesa',  
        })
        
        # Verifica che il modello RichiestaAdozione sia stato creato
        self.assertTrue(RichiestaAdozione.objects.filter(utente= self.user, animale=self.animale).exists())

        # Verifica che il template di successo sia stato utilizzato
        self.assertTemplateUsed(response, 'successoRichiestaAdozione.html')

class AnimalFilterTest(TestCase):
    def test_animal_filter(self):
        # Crea alcune istanze di Animale
        animal1 = Animale.objects.create(specie='Gatto', razza='GattoBlu', età=12, descrizione="Carino")
        animal2 = Animale.objects.create(specie='Cane', razza='Labrador', età=12, descrizione="Cattivo")
        animal3 = Animale.objects.create(specie='Cavallo', razza='PSI', età=22, descrizione="Calmo")
        animal4 = Animale.objects.create(specie='Cane', razza='Pitbull', età=15, descrizione="Tranquillo")

        # Filtra gli animali per specie 'Cane'
        filter_data_specie = {'specie': 'Cane'}
        animal_filter1 = AnimalFilter(data=filter_data_specie, queryset=Animale.objects.all())
        filtered_animals_specie = animal_filter1.qs
        self.assertIn(animal2, filtered_animals_specie)
        self.assertIn(animal4, filtered_animals_specie)
        self.assertNotIn(animal3, filtered_animals_specie)

        #filta gli animali per età
        filter_data_età = {'età': '12'}
        animal_filter2= AnimalFilter(data=filter_data_età, queryset=Animale.objects.all())
        filtered_animals_età = animal_filter2.qs

        self.assertIn(animal1, filtered_animals_età)
        self.assertIn(animal2, filtered_animals_età)
        self.assertNotIn(animal3, filtered_animals_età)

        #filta gli animali per razza
        filter_data_razza = {'razza': 'PSI'}
        animal_filter3= AnimalFilter(data=filter_data_razza, queryset=Animale.objects.all())
        filtered_animals_razza = animal_filter3.qs

        self.assertIn(animal3, filtered_animals_razza)
        self.assertNotIn(animal1, filtered_animals_razza)
        self.assertNotIn(animal2, filtered_animals_razza)

        #filta gli animali per descrizione
        filter_data_descrizione = {'descrizione': 'Carino'}
        animal_filter4= AnimalFilter(data=filter_data_descrizione, queryset=Animale.objects.all())
        filtered_animals_descrizione = animal_filter4.qs
        self.assertIn(animal1, filtered_animals_descrizione)
        self.assertNotIn(animal3, filtered_animals_descrizione)
        self.assertNotIn(animal2, filtered_animals_descrizione)

class RichiestaFilterTest(TestCase):
    def test_richiesta_filter(self):
        # Crea alcune istanze di RichiestaAdozione
        utente1 = User.objects.create_user(username='Oingo', password='Password_123')
        utente2 = User.objects.create_user(username='Oingo1', password='Password_123')
        animal1 = Animale.objects.create(ID_animale=1, specie='Gatto', razza='GattoBlu', età=12, descrizione="Carino")
        animal2 = Animale.objects.create(ID_animale=2, specie='Cane', razza='Labrador', età=12, descrizione="Cattivo")

        richiesta1 = RichiestaAdozione.objects.create(utente=utente2, animale=animal1,
                                                      nomeCognome='Richiesta1', indirizzo="Via Colombo",
                                                      emailNumeroDiTelefono="n@email.it", richiesta='In attesa')
        richiesta2 = RichiestaAdozione.objects.create(utente=utente1, animale=animal1,
                                                      nomeCognome='Richiesta2', indirizzo="Via Petrarca",
                                                      emailNumeroDiTelefono="3356951111", richiesta='In attesa')

        # Filtra le richieste per nomeCognome
        filter_data_ID_richiestaAdozione = {'nomeCognome': 'Richiesta1'}
        richiesta_filter_ID = RichesteFilter(data=filter_data_ID_richiestaAdozione, queryset=RichiestaAdozione.objects.all())
        filtered_richieste_ID = richiesta_filter_ID.qs
        self.assertIn(richiesta1, filtered_richieste_ID)
        self.assertNotIn(richiesta2, filtered_richieste_ID)

        # Filtra le richieste per indirizzo
        filter_data_ID_richiestaAdozione = {'indirizzo': 'Via Petrarca'}
        richiesta_filter_ID = RichesteFilter(data=filter_data_ID_richiestaAdozione, queryset=RichiestaAdozione.objects.all())
        filtered_richieste_ID = richiesta_filter_ID.qs
        self.assertIn(richiesta2, filtered_richieste_ID)
        self.assertNotIn(richiesta1, filtered_richieste_ID)

        # Filtra le richieste per email e numero di telefono
        filter_data_ID_richiestaAdozione = {'emailNumeroDiTelefono': '3356951111'}
        richiesta_filter_ID = RichesteFilter(data=filter_data_ID_richiestaAdozione, queryset=RichiestaAdozione.objects.all())
        filtered_richieste_ID = richiesta_filter_ID.qs
        self.assertIn(richiesta2, filtered_richieste_ID)
        self.assertNotIn(richiesta1, filtered_richieste_ID)

#test unitario per il login
class LoginTest(TestCase):
    #SetUp con la creazione di un user come esempio 
    def setUp(self):
        self.user = User.objects.create_user(username='Oingo', password='Password_123')

    #Test per il login corretto 
    def test_login_valid_user(self):
        response = self.client.post(reverse('login'), {'username': 'Oingo', 'password': 'Password_123'})
        # Verifica che la risposta reindirizzi all'URL di successo
        self.assertRedirects(response, reverse('home'))
        # Verifica che l'utente sia autenticato
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_user(self):
        response = self.client.post(reverse('login'), {'username': 'Oingo', 'password': 'Password_12'})
        # Verifica che la risposta reindirizzi alla stessa pagina di login enon alla home come nel caso precedente
        self.assertEqual(response.status_code, 200) 
        # Verifica che l'utente non sia autenticato
        self.assertFalse(response.wsgi_request.user.is_authenticated)

#test per la registrazione di un nuovo utente
class RegistrationTest(TestCase):
    def test_registration_valid_user(self):
        data = {
            'username': 'NewUser',
            'password1': 'NewPassword123',
            'password2': 'NewPassword123',
        }
        response = self.client.post(reverse('register'), data)
        # Verifica che l'utente sia stato creato
        self.assertTrue(User.objects.filter(username='NewUser').exists())

    def test_registration_invalid_user(self):
        data = {
           'username': 'NewUser',
            'password1': 'NewPassword123',
           'password2': 'DifferentPassword',  # Password diversa da quella inserita sopra
        }
        response = self.client.post(reverse('register'), data)
        # Verifica che la pagina di registrazione sia stata visualizzata nuovamente
        self.assertEqual(response.status_code, 200)
        # Verifica che l'utente non sia stato creato
        self.assertFalse(User.objects.filter(username='NewUser').exists())

#Test che simula la risposta da parte di un Admin per le richieste di adozione accettandole o rifiutandole
class AccettaRifiutaAdozioneTest(TestCase):
    def test_accetta_richiesta(self):
        # Crea un utente e un animale di esempio
        utente = User.objects.create_superuser(username='Utente1', password='Password_123')
        animale = Animale.objects.create(specie='Gatto', razza='GattoBlu', età=12, descrizione="Carino")

        # Crea una richiesta di adozione
        richiesta = RichiestaAdozione.objects.create(utente=utente, animale=animale,
                                                      nomeCognome='Richiesta1', indirizzo="Via Colombo",
                                                      emailNumeroDiTelefono="n@email.it", richiesta='In attesa')
        # Verifica che l'animale esiste
        self.assertTrue(Animale.objects.filter(specie='Gatto').exists())

        # Effettua l'accesso come utente con privilegi di amministratore
        self.client.login(username='Utente1', password='Password_123')

        # Chiama l'URL per accettare la richiesta
        url = reverse('accetta_rifiuta_view', args=[richiesta.ID_richiestaAdozione, 'true'])
        response = self.client.post(url)

        # Verifica che la pagina abbia reindirizzato correttamente
        self.assertRedirects(response, reverse('success_page_for_acceptance'))

        # Verifica che l'animale sia stato eliminato
        self.assertFalse(Animale.objects.filter(specie='Gatto').exists())
    
    def test_rifiuta_richiesta(self):
        # Crea un utente e un animale di esempio
        utente = User.objects.create_superuser(username='Utente1', password='Password_123')
        animale = Animale.objects.create(specie='Gatto', razza='GattoBlu', età=12, descrizione="Carino")

        # Crea una richiesta di adozione
        richiesta = RichiestaAdozione.objects.create(utente=utente, animale=animale,
                                                      nomeCognome='Richiesta1', indirizzo="Via Colombo",
                                                      emailNumeroDiTelefono="n@email.it", richiesta='In attesa')
        # Verifica che l'animale esiste
        self.assertTrue(Animale.objects.filter(specie='Gatto').exists())

        # Effettua l'accesso come utente con privilegi di amministratore
        self.client.login(username='Utente1', password='Password_123')

        # Chiama l'URL per rifiutare la richiesta
        url = reverse('accetta_rifiuta_view', args=[richiesta.ID_richiestaAdozione, 'false'])
        response = self.client.post(url)

        # Verifica che la pagina abbia reindirizzato correttamente
        self.assertRedirects(response, reverse('success_page_for_rejection'))

        # Verifica che la richiesta sia stata eliminato
        self.assertFalse(RichiestaAdozione.objects.filter(nomeCognome='Richiesta1').exists())


