from django.test import TestCase
from .models import Animale, RichiestaAdozione
from django.contrib.auth.models import User
from django.urls import reverse
from adozione.filters import AnimalFilter, RichesteFilter
from django.contrib.auth import login, logout

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


####################################################################################
# test di accettazione lato admin
# test ok
class LoginAdminTest(TestCase):
    def setUp(self):
        #drivers_dir = os.path.join(os.path.dirname(__file__),'drivers')
        #chrome_driver_path = os.path.join(drivers_dir,'chromedriver')
        self.browser = webdriver.Chrome()
        self.live_server_url= "http://localhost:8000"
        self.aux_url= "?next=/home/"
        super(LoginAdminTest, self).setUp()
        
    def tearDown(self):
        self.browser.quit()
        super(LoginAdminTest,self).tearDown()
    
    def test_login_amministratore_successo(self):
        self.browser.get(self.live_server_url)
        time.sleep(3)
        self.browser.find_element('name','username').send_keys('Admin')
        self.browser.find_element('name','password').send_keys('Admin')
        time.sleep(1)
        text = "Login"
        login_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
        login_btn.click()
        time.sleep(3)
        auxUrl = self.live_server_url + reverse('home_amministratore') + self.aux_url
        self.assertEquals(self.browser.current_url,auxUrl)
    
    def test_login_amministratore_errore(self):
        self.browser.get(self.live_server_url)
        time.sleep(3)
        self.browser.find_element('name','username').send_keys('Admin')
        time.sleep(1)
        self.browser.find_element('name','password').send_keys('wrong password')
        time.sleep(1)
        text = "Login"
        login_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
        login_btn.click()
        time.sleep(3)
        auxUrl = self.live_server_url + "/"
        self.assertEquals(self.browser.current_url,auxUrl)
        errorElem = self.browser.find_element(By.CLASS_NAME,"errorlist")
        self.assertTrue(errorElem.is_displayed())

# test ok
class HomeAdminTest(TestCase):
    #L’amministratore visualizza la lista delle richieste di 
    # adozione con i dati relativi all’utente che ha fatto la richiesta e 
    # all’animale scelto. L’amministratore premendo i tasti rifiuta o accetta 
    # decide l’esito della richiesta di adozione, la richiesta relativa viene 
    # cancellata dalla lista
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.live_server_url= "http://127.0.0.1:8000"
        super(HomeAdminTest, self).setUp()
        
    def tearDown(self):
        self.browser.quit()
        super(HomeAdminTest,self).tearDown()
    
    
    def login(self):
        self.browser.get(self.live_server_url)
        time.sleep(3)
        self.browser.find_element('name','username').send_keys('Admin')
        self.browser.find_element('name','password').send_keys('Admin')
        time.sleep(1)
        text = "Login"
        login_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
        login_btn.click()
        time.sleep(3)
    
    # ok
    def test_accetta_richiesta_adozione(self):
        self.login()
        time.sleep(4)
        # sono nella pagina home amministratore
        text_to_find = "Accetta"
        first_tr = self.browser.find_element(By.XPATH,"//tbody//tr[1]")
        id_elemento= first_tr.get_attribute("id")
        accetta_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        accetta_btn.click()
        time.sleep(3)
        aux_url= self.live_server_url + "/accetta_success/"
        self.assertEquals(self.browser.current_url,aux_url)

        # controllo sulla pagina esito
        testo= "La richiesta è stata accettata"
        try:
            esito = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{testo}")]')
            assert True
        except NoSuchElementException:
            assert False

        # controllo che la richiesta sia stata cancellata dalla lista
        testo_btn_home= "Home"
        home_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{testo_btn_home}")]')
        home_btn.click()
        time.sleep(3)
        string= "//tbody" +"//tr[@id=\"" + id_elemento + "\"]"
        try:
            tr_by_id = self.browser.find_element(By.XPATH,string)
        except NoSuchElementException:
            assert True
    
    # ok
    def test_rifiuta_richiesta_adozione(self):
        self.login()
        time.sleep(4)
        # sono nella pagina home amministratore
        text_to_find = "Rifiuta"
        first_tr = self.browser.find_element(By.XPATH,"//tbody//tr[1]")
        id_elemento= first_tr.get_attribute("id")
        accetta_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        accetta_btn.click()
        time.sleep(3)
        aux_url= self.live_server_url +"/rifiuta_success/"
        self.assertEquals(self.browser.current_url,aux_url)
        # controllo sulla pagina esito
        testo= "La richiesta è stata rifiutata"
        try:
            esito = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{testo}")]')
            assert True
        except NoSuchElementException:
            assert False

        # controllo che la richiesta sia stata cancellata dalla lista
        testo_btn_home= "Home"
        home_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{testo_btn_home}")]')
        home_btn.click()
        time.sleep(3)
        string= "//tbody" +"//tr[@id=\"" + id_elemento + "\"]"
        try:
            tr_by_id = self.browser.find_element(By.XPATH,string)
        except NoSuchElementException:
            assert True

# test ok
class FilterAdminTest(TestCase):
    # L’amministratore premendo il tasto filtra può filtrare il contenuto 
    # della lista delle richieste in base alla specie e alla razza dell’animale 
    # scelto. Se non vi sono corrispondenze non si visualizza nessuna richiesta
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.live_server_url= "http://127.0.0.1:8000"
        super(FilterAdminTest, self).setUp()
        
    def tearDown(self):
        self.browser.quit()
        super(FilterAdminTest,self).tearDown()

    def login(self):
        self.browser.get(self.live_server_url)
        time.sleep(3)
        self.browser.find_element('name','username').send_keys('Admin')
        self.browser.find_element('name','password').send_keys('Admin')
        time.sleep(1)
        text = "Login"
        login_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
        login_btn.click()
        time.sleep(3)
    
    # ok
    def test_filtro_lista(self):
        self.login()
        # click sul pulsante lista animali
        # controllo url deve essere: http://localhost:8000/lista_animaliAmministratore/
        text_to_find = "Lista Animali"
        lista_animali_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        lista_animali_btn.click()
        aux_url= self.live_server_url + "/lista_animaliAmministratore/"
        self.assertEquals(self.browser.current_url,aux_url)
        # selezione filtro per specie e invio
        filtro_specie= "Cane"
        self.browser.find_element(By.ID,'id_specie').send_keys(filtro_specie)
        time.sleep(3)
        text_to_find = " Cerca "
        cerca_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        cerca_btn.click()
        # controllo che il filtro abbia avuto successo
        # prendo tutte le tr e controllo che il testo all'interno della colonna specie sia
        # uguale al filtro
        time.sleep(4)
        lista_tr = self.browser.find_elements(By.XPATH, "//tr")
        for tr in lista_tr:
            colonna_specie = tr.find_element(By.XPATH, "//td[1]")
            testo_colonna_specie = colonna_specie.text
            self.assertEquals(testo_colonna_specie,filtro_specie)
        
    # ok
    def test_filtro_lista_vuota(self):
        self.login()
        # click sul pulsante lista animali
        # controllo url deve essere: http://localhost:8000/lista_animaliAmministratore/
        text_to_find = "Lista Animali"
        lista_animali_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        lista_animali_btn.click()
        aux_url= self.live_server_url + "/lista_animaliAmministratore/"
        self.assertEquals(self.browser.current_url,aux_url)
        # selezione filtro per specie e invio
        filtro_specie= "questa specie non esiste"
        
        self.browser.find_element(By.ID,'id_specie').send_keys(filtro_specie)
        time.sleep(3)
        text_to_find = " Cerca "
        cerca_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        cerca_btn.click()
        # controllo che il filtro non abbia avuto successo
        # prendo tutte le tr e controllo che l'array di tr abbia lunghezza zero
        time.sleep(3)
        lista_tr = self.browser.find_elements(By.XPATH, "//tbody//tr")
        self.assertEquals(0,len(lista_tr))

# test ok
class ListAnimalAdminTest(TestCase):
    # L’amministratore premendo il tasto lista animali visualizza la lista 
    # degli animali adottabili, può modificare un elemento della lista 
    # cliccando sul pulsante modifica.
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.live_server_url= "http://127.0.0.1:8000"
        super(ListAnimalAdminTest, self).setUp()
        
    def tearDown(self):
        self.browser.quit()
        super(ListAnimalAdminTest,self).tearDown()
    
    def login(self):
        self.browser.get(self.live_server_url)
        time.sleep(3)
        self.browser.find_element('name','username').send_keys('Admin')
        self.browser.find_element('name','password').send_keys('Admin')
        time.sleep(1)
        text = "Login"
        login_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
        login_btn.click()
        time.sleep(3)
    
    # ok!
    def go_to_lista_animali(self):
        text_to_find = "Lista Animali"
        lista_animali_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        lista_animali_btn.click()
        time.sleep(3)
    
    # da testare
    def test_modifica_animale(self):
        self.login()
        self.go_to_lista_animali()
        # seleziono la prima tr
        first_tr = self.browser.find_element(By.XPATH,"//tbody//tr[1]")
        # salvo l'id dell'animale 
        id_animale = first_tr.get_attribute("id")
        # seleziono il primo pulsante modifica
        text_to_find = "Modifica"
        modifica_btn = first_tr.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        # click sul pulsante
        modifica_btn.click()
        # controllo di essere nella pagina corretta
        aux_url= self.live_server_url + "/modifica_animale/" + id_animale + "/"
        self.assertEquals(self.browser.current_url,aux_url)
        # modifico
        self.browser.find_element('name','specie').clear()
        self.browser.find_element('name','specie').send_keys('test')
        self.browser.find_element('name','razza').clear()
        self.browser.find_element('name','razza').send_keys('test')
        self.browser.find_element('name','età').clear()
        self.browser.find_element('name','età').send_keys('1')
        self.browser.find_element('name','descrizione').clear()
        self.browser.find_element('name','descrizione').send_keys('test')
        time.sleep(4)
        # click su invia
        text = "Salva Modifiche"
        salva_modifiche_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
        salva_modifiche_btn.click()
        time.sleep(3)
        # torno alla lista animali
        # controllo che la modifica sia stata effettuata
        # prendo la tr con id = id_animale
        # controllo che i td siano corretti
        stringa = f'//tbody//tr[@id="{id_animale}"]'
        tr_post_mod = self.browser.find_element(By.XPATH,stringa)
        specie = tr_post_mod.find_element(By.XPATH,"//td[1]").text
        razza = tr_post_mod.find_element(By.XPATH,"//td[2]").text
        eta = tr_post_mod.find_element(By.XPATH,"//td[3]").text
        descrizione = tr_post_mod.find_element(By.XPATH,"//td[4]").text
        self.assertEquals(specie,"test")
        self.assertEquals(razza,"test")
        self.assertEquals(eta,"1")
        self.assertEquals(descrizione,"test")

# test ok
class AddAnimalTest(TestCase):
     # L’amministratore cliccando sul pulsante aggiungi animale può 
     # inserendo i dati relativi all’animale inserire un nuovo animale nella 
     # lista degli animali adottabili. Se la compilazione dei campi e corretta e 
     # completa l’animale viene aggiunto alla lista, altrimenti si visualizza l’errore.
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.live_server_url= "http://127.0.0.1:8000"
        super(AddAnimalTest, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(AddAnimalTest,self).tearDown()

    def login(self):
        self.browser.get(self.live_server_url)
        time.sleep(3)
        self.browser.find_element('name','username').send_keys('Admin')
        self.browser.find_element('name','password').send_keys('Admin')
        time.sleep(1)
        text = "Login"
        login_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
        login_btn.click()
        time.sleep(3)

    # ok!
    def go_to_lista_animali(self):
        text_to_find = "Lista Animali"
        lista_animali_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        lista_animali_btn.click()
        time.sleep(3)

    # da testare
    def test_add_successo(self):
        self.login()
        self.go_to_lista_animali()
        # click sul pulsante aggiungi animale
        text_to_find = "Aggiungi animale"
        aggiungi_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        aggiungi_btn.click()
        time.sleep(3)
       # controllo di essere nella pagina corretta
        aux_url= self.live_server_url + "/aggiungiAnimale/"
        self.assertEquals(self.browser.current_url,aux_url)
        # compilazione form
        self.browser.find_element('name','specie').send_keys('SpecieTest')
        self.browser.find_element('name','razza').send_keys('RazzaTest')
        self.browser.find_element('name','età').clear()
        self.browser.find_element('name','età').send_keys('1')
        self.browser.find_element('name','descrizione').send_keys('DescrizioneTest')
        # click su invia
        time.sleep(3)
        testo_btn_invia = "Aggiungi Animale"
        invia_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{testo_btn_invia}")]')
        invia_btn.click()
        time.sleep(3)
        # controllo di essere nella lista animali amministratore
        aux_url= self.live_server_url + "/lista_animaliAmministratore/"
        self.assertEquals(self.browser.current_url,aux_url)
        # controllo che l'animale sia stato aggiunto
        # trova tutti i tr nella pagina
        lista_tr = self.browser.find_elements(By.XPATH, "//tr")
        # seleziona l'ultimo
        for tr in lista_tr:
            ultimo_tr = tr

        specie = ultimo_tr.find_element(By.XPATH,".//td[1]").text
        razza = ultimo_tr.find_element(By.XPATH,".//td[2]").text
        eta = ultimo_tr.find_element(By.XPATH,".//td[3]").text
        descrizione = ultimo_tr.find_element(By.XPATH,".//td[4]").text
        self.assertEquals(specie,"SpecieTest")
        self.assertEquals(razza,"RazzaTest")
        self.assertEquals(eta,"1")
        self.assertEquals(descrizione,"DescrizioneTest")

####################################################################################
# test di accettazione lato client
# test ok
class LoginUserTest(TestCase):
    # L’utente deve inserire username e password scelti in fase 
    # di registrazione per poter accedere al sistema. 
    # Se la password o lo username non sono corretti viene 
    # segnalato l’errore. Se i dati sono corretti l’utente 
    # può vedere la lista di animali adottabili.
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.live_server_url= "http://127.0.0.1:8000"
        super(LoginUserTest, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(LoginUserTest,self).tearDown()
    
    #da testare
    def test_login_user_successo(self):
        self.browser.get(self.live_server_url)
        time.sleep(3)
        self.browser.find_element('name','username').send_keys('Oingo')
        self.browser.find_element('name','password').send_keys('Password_123')
        time.sleep(1)
        text = "Login"
        login_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
        login_btn.click()
        time.sleep(3)
        auxUrl = self.live_server_url + reverse('home')
        self.assertEquals(self.browser.current_url,auxUrl)
    
    # da testare
    def test_login_login_errore(self):
        self.browser.get(self.live_server_url)
        time.sleep(3)
        self.browser.find_element('name','username').send_keys('Oingo')
        time.sleep(1)
        self.browser.find_element('name','password').send_keys('wrong password')
        time.sleep(1)
        text = "Login"
        login_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
        login_btn.click()
        time.sleep(3)
        auxUrl = self.live_server_url + "/"
        self.assertEquals(self.browser.current_url,auxUrl)
        errorElem = self.browser.find_element(By.CLASS_NAME,"errorlist")
        self.assertTrue(errorElem.is_displayed())

# test ok
class UserRegTest(TestCase):
    #L’utente deve inserire username e password per 
    # poter effettuare la registrazione. Se i dati 
    # non sono corretti, un messaggio informa l’utente;
    # se i dati sono corretti, la procedura di 
    # registrazione va a buon fine.
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.live_server_url= "http://127.0.0.1:8000"
        super(UserRegTest, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(UserRegTest,self).tearDown()
    
    # ok
    def test_register_successo(self):
        self.browser.get(self.live_server_url)
        # click sul pulsante register
        text_to_find = "Register"
        cerca_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        cerca_btn.click()
        time.sleep(3)
        # compilo form
        self.browser.find_element('name','username').send_keys('Test3')
        self.browser.find_element('name','password1').send_keys('Password_1234')
        self.browser.find_element('name','password2').send_keys('Password_1234')
        # click su invia  il name del pulsante è Create User
        time.sleep(1)
        invia_btn = self.browser.find_element("name","Create User")
        invia_btn.click()
        time.sleep(3)
        # controllo messaggio di successo
        try:
            text = "Richiesta registrazione inviata!"
            self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
            assert True
        except NoSuchElementException:
            assert False
        # controllo di essere nella pagina per il login
        aux_url= self.live_server_url +"/register/"
        self.assertEquals(self.browser.current_url,aux_url)
        #click su home
        text_to_find = "Home"
        home_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        home_btn.click()
        time.sleep(3)
        # compilo il form
        self.browser.find_element('name','username').send_keys('Test3')
        time.sleep(1)
        self.browser.find_element('name','password').send_keys('Password_1234')
        time.sleep(4)
        # click su login
        text = "Login"
        login_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
        login_btn.click()
        time.sleep(3)
        # controllo che l'url di arrivo sia http://127.0.0.1:8000/home/
        aux_url= self.live_server_url + "/home/?next=/home_amministratore/"
        self.assertEquals(self.browser.current_url,aux_url)

# test ok
class FormAdozioneTest(TestCase):
    # L’utente compila i campi nome, cognome, indirizzo, 
    # lavoro, numero di telefono, con i propri dati per inviare 
    # la richiesta di adozione relativa all’animale scelto.
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.live_server_url= "http://127.0.0.1:8000"
        super(FormAdozioneTest, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(FormAdozioneTest,self).tearDown()
    
    # da testare
    def loginUtente(self):
        self.browser.get(self.live_server_url)
        time.sleep(3)
        self.browser.find_element('name','username').send_keys('Oingo')
        self.browser.find_element('name','password').send_keys('Password_123')
        time.sleep(1)
        text = "Login"
        login_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
        login_btn.click()
        time.sleep(3)
    
    # da testare
    def loginAdmin(self):
        self.browser.get(self.live_server_url)
        time.sleep(3)
        self.browser.find_element('name','username').send_keys('Admin')
        self.browser.find_element('name','password').send_keys('Admin')
        time.sleep(1)
        text = "Login"
        login_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
        login_btn.click()
        time.sleep(3)
    
    # da testare
    def test_adozione_form(self):
        self.loginUtente()
        # selezione il primo tr
        first_tr = self.browser.find_element(By.XPATH,"//tbody//tr[1]")
        id_animale= first_tr.get_attribute("id")
        # click sul bottone adotta
        text_to_find = "adotta"
        adotta_btn = first_tr.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        adotta_btn.click()
        # controllo che sia nella pagina "http://127.0.0.1:8000/adotta/id_dell'animale/"
        aux_url= self.live_server_url + "/adotta/" + id_animale + "/"
        self.assertEquals(self.browser.current_url,aux_url)
        # compilo il form
        self.browser.find_element('name','nomeCognome').send_keys('TestNomeCognome')
        self.browser.find_element('name','indirizzo').send_keys('TestIndirizzo')
        self.browser.find_element('name','emailNumeroDiTelefono').send_keys('333444555')
        # click su invia
        text_to_find = "Invia"
        cerca_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        cerca_btn.click()
        # controlla che venga stampato il messaggio ""Richiesta di adozione inviata!"
        try:
            text = "Richiesta di adozione inviata!"
            self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
            assert True
        except NoSuchElementException:
            assert False
        # login come admin
        self.loginAdmin()
        # controllo che la richiaesta sia stata inserita
        lista_tr = self.browser.find_elements(By.XPATH, "//tr")
        # seleziona l'ultimo
        for tr in lista_tr:
            ultimo_tr = tr
        nomeCognome = ultimo_tr.find_element(By.XPATH,"//td[1]").text
        indirizzo = ultimo_tr.find_element(By.XPATH,"//td[2]").text
        self.assertEquals(nomeCognome,"TestNomeCognome")
        self.assertEquals(indirizzo,"TestIndirizzo")

# test ok
class HomeUtenteTest(TestCase):

    # L’utente visualizza la lista con gli animali adottabili. 
    # L'utente clicca sul bottone adotta relativo all’animale 
    # selezionato che lo reindirizza alla compilazione del form 
    # per l’adozione.
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.live_server_url= "http://127.0.0.1:8000"
        super(HomeUtenteTest, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(HomeUtenteTest,self).tearDown()
    
    # ok
    def loginUtente(self):
        self.browser.get(self.live_server_url)
        time.sleep(3)
        self.browser.find_element('name','username').send_keys('Oingo')
        self.browser.find_element('name','password').send_keys('Password_123')
        time.sleep(1)
        text = "Login"
        login_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
        login_btn.click()
        time.sleep(3)
    
    # ok
    def test_adotta_reindirizzamento(self):

        self.loginUtente()
        # trova primo tr
        first_tr = self.browser.find_element(By.XPATH,"//tbody//tr[1]")
        id_animale= first_tr.get_attribute("id")
        # click sul bottone adotta
        text_to_find = "adotta"
        adotta_btn = first_tr.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        adotta_btn.click()
        time.sleep(3)
        # controllo che sia nella pagina "http://127.0.0.1:8000/adotta/id_dell'animale/"
        aux_url= self.live_server_url + "/adotta/" + id_animale + "/"
        self.assertEquals(self.browser.current_url,aux_url)

# test ok
class FiltriUtenteTest(TestCase):
    # L’utente filtra la lista degli animali adottabili in base alla 
    # specie o alla razza dell’animale. Se la specie o la razza 
    # inserita non è presente tra gli animali adottabili l’utente 
    # non visualizza nessun animale.
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.live_server_url= "http://127.0.0.1:8000"
        super(FiltriUtenteTest, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(FiltriUtenteTest,self).tearDown()
    
    # da testare
    def loginUtente(self):
        self.browser.get(self.live_server_url)
        time.sleep(3)
        self.browser.find_element('name','username').send_keys('Oingo')
        self.browser.find_element('name','password').send_keys('Password_123')
        time.sleep(1)
        text = "Login"
        login_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
        login_btn.click()
        time.sleep(3)

    # da testare
    def test_filtri_utente_lista(self):
        self.loginUtente()
        # compilo form
        filtro_specie= "Cane"
        self.browser.find_element(By.ID,'id_specie').send_keys(filtro_specie)
        text_to_find = " Cerca "
        cerca_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        cerca_btn.click()
        # controllo che il filtro abbia avuto successo
        # prendo tutte le tr e controllo che il testo all'interno della colonna specie sia
        # uguale al filtro
        lista_tr = self.browser.find_elements(By.XPATH, "//tr")
        for tr in lista_tr:
            colonna_specie = tr.find_element(By.XPATH, "//td[1]")
            testo_colonna_specie = colonna_specie.text
            self.assertEquals(testo_colonna_specie,filtro_specie)
    
    # da testare
    def test_filtri_utente_lista_vuota(self):
        self.loginUtente()
        # compilo form
        filtro_specie= "questo filtro non esiste"
        self.browser.find_element(By.ID,'id_specie').send_keys(filtro_specie)
        text_to_find = " Cerca "
        cerca_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        cerca_btn.click()
        # controllo che il filtro non abbia avuto successo
        # prendo tutte le tr e controllo che l'array di tr abbia lunghezza zero
        lista_tr = self.browser.find_elements(By.XPATH, "//tbody//tr")
        self.assertEquals(0,len(lista_tr))

# test ok
class LogoutUtenteTest(TestCase):
    # L’utente clicca sul pulsante Logout che effettua il logout 
    # dell’utente e reindirizza l’utente alla pagina di login
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.live_server_url= "http://127.0.0.1:8000"
        self.aux_url= "/?next=/home/"
        super(LogoutUtenteTest, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(LogoutUtenteTest,self).tearDown()
    
    # ok
    def loginUtente(self):
        self.browser.get(self.live_server_url)
        time.sleep(3)
        self.browser.find_element('name','username').send_keys('Oingo')
        self.browser.find_element('name','password').send_keys('Password_123')
        time.sleep(1)
        text = "Login"
        login_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text}")]')
        login_btn.click()
        time.sleep(3)
    
    # ok
    def test_logout(self):
        self.loginUtente()
        text_to_find = "Logout"
        logout_btn = self.browser.find_element(By.XPATH, f'//*[contains(text(), "{text_to_find}")]')
        logout_btn.click()
        time.sleep(3)
        # controllo reindirizzamento a  "http://127.0.0.1:8000/?next=/home/"
        auxUrl = self.live_server_url + self.aux_url
        self.assertEquals(self.browser.current_url,auxUrl)
