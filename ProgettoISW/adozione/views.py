from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User  # Assicurati di importare il modello User
from .models import Animale, RichiestaAdozione
from .forms import RichiestaAdozioneForm, ModificaAnimaleForm, AggiungiAnimaleForm
from .filters import AnimalFilter, RichesteFilter
from django.contrib.auth.decorators import user_passes_test, login_required


import logging

# Configura il logger
logging.basicConfig(filename='myapp.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Imposta il livello a DEBUG per il logger

@user_passes_test(lambda u: not u.is_superuser, login_url='home_amministratore')
@login_required(login_url='login')
def home(request):
    animali = Animale.objects.all() 
    logger.debug("home")
    myFilter = AnimalFilter(request.GET, queryset=animali)
    animali = myFilter.qs

    context = {'animali': animali, 'myFilter': myFilter}
    return render(request, "home.html", context)



@user_passes_test(lambda u: u.is_superuser, login_url='home')
def home_amministratore(request):
    richieste = RichiestaAdozione.objects.all()

    myFilter = RichesteFilter(request.GET, queryset=richieste)
    richieste = myFilter.qs
    logger.debug("homeAmmm")

    context = {'richieste':richieste, 'myFilter': myFilter}
    return render(request,'home_amministratore.html',context)

def lista_animaliAmministratore(request):
    animali = Animale.objects.all() 

    myFilter = AnimalFilter(request.GET, queryset=animali)
    animali = myFilter.qs

    context = {'animali': animali, 'myFilter': myFilter}
    return render(request, "lista_animaliAmministratore.html", context)

#invio della richiesta di adozione prendendo l'id dell'animale selezionato e lo user loggato al momento dell'invio della richiesta
def adotta(request, animale_id):
    animale = Animale.objects.get(pk=animale_id)

    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data['animale'] = animale.ID_animale  
        form_data['utente'] = request.user 
        form = RichiestaAdozioneForm(form_data)
        if form.is_valid():
            richiesta_adozione = form.save(commit=False)
            richiesta_adozione.animale = animale
            richiesta_adozione.utente = request.user
            richiesta_adozione.save()        
            logger.debug("Richiesta di adozione creata con successo")          
            if request.POST.get('azione') == 'accetta':
                animale.delete()

            return render(request, 'successoRegistrazione.html')
        else:
            logger.debug("Form non valido")
    else:
        form = RichiestaAdozioneForm(initial={'animale': animale_id, 'utente': request.user})
    
    context = {'animale': animale, 'form': form}
    return render(request, 'adotta.html', context)

#view per aggiungere un nuovo animale alla lista
def aggiungiAnimale(request):
    form = AggiungiAnimaleForm()

    if request.method == 'POST':
        form = AggiungiAnimaleForm(request.POST)
        if form.is_valid():
            form.save()
            logger.debug("OK")
            #Reindirizzo alla pagina lista_animaliAmministratore dopo aver aggiunto l'animale
            return redirect('lista_animaliAmministratore')
        else:
            logger.debug("ERRORE")

    else:
            form = AggiungiAnimaleForm()
    
    return render(request, 'aggiungi_animale.html', {'form': form})

#View per modificare gli animali (dalla pagina lista_AnimaliAmministratore)
def modifica_animale(request, animale_id):
    animale = Animale.objects.get(pk=animale_id)

    form = ModificaAnimaleForm(instance=animale)

    if request.method == 'POST':
        form = ModificaAnimaleForm(request.POST, instance = animale)
        if form.is_valid():
            form.save()
            return redirect('lista_animaliAmministratore')

    return render(request, 'modificaAnimale.html', {'form': form})


def logout_view(request):
    logout(request)
    return  redirect('home')

def registerPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Esegui altre operazioni dopo il salvataggio
            return  render(request, 'successoRegistrazione.html')  # Redirigi a una pagina di successo
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'register.html', context)

def accetta_rifiuta_view(request, richiesta_id, risultato):
        azione = risultato.lower() == 'true'
        richiesta = RichiestaAdozione.objects.get(pk=richiesta_id)
        ID_animale = int(richiesta.animale.ID_animale)
        animale = Animale.objects.get(pk=ID_animale)
        if azione:
            # Esegui l'azione di accettazione (ad esempio, cambia lo stato della richiesta)
            
            richiesta.richiesta = 'Accettata'
            richiesta.save()

            # Elimina l'animale

            animale.delete()
            render(request, 'successoRegistrazione.html')  # Reindirizza a una pagina di successo
        else:
            # Esegui l'azione di rifiuto (ad esempio, cambia lo stato della richiesta)
            richiesta.delete()
            render(request, 'successoRegistrazione.html')  # Reindirizza a una pagina di successo
        return render(request, 'successoRegistrazione.html')  # Reindirizza a una pagina di successo

