from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .models import Animale, RichiestaAdozione
from .forms import RichiestaAdozioneForm, ModificaAnimaleForm, AggiungiAnimaleForm
from .filters import AnimalFilter, RichesteFilter
from django.contrib.auth.decorators import user_passes_test, login_required



@user_passes_test(lambda u: not u.is_superuser, login_url='home_amministratore')
@login_required(login_url='login')
def home(request):
    animali = Animale.objects.all() 
    myFilter = AnimalFilter(request.GET, queryset=animali)
    animali = myFilter.qs
    context = {'animali': animali, 'myFilter': myFilter}
    return render(request, "home.html", context)

@user_passes_test(lambda u: u.is_superuser, login_url='home')
def home_amministratore(request):
    richieste = RichiestaAdozione.objects.all()
    myFilter = RichesteFilter(request.GET, queryset=richieste)
    richieste = myFilter.qs
    context = {'richieste':richieste, 'myFilter': myFilter}
    return render(request,'home_amministratore.html',context)

def lista_animaliAmministratore(request):
    animali = Animale.objects.all() 
    myFilter = AnimalFilter(request.GET, queryset=animali)
    animali = myFilter.qs

    context = {'animali': animali, 'myFilter': myFilter}
    return render(request, "lista_animaliAmministratore.html", context)

#invio della richiesta di adozione prendendo l'id dell'animale selezionato e lo user 
#loggato al momento dell'invio della richiesta
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
            if request.POST.get('azione') == 'accetta':
                animale.delete()

            return render(request, 'successoRichiestaAdozione.html')
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
            #Reindirizzo alla pagina lista_animaliAmministratore dopo aver aggiunto l'animale
            return redirect('lista_animaliAmministratore')

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

#view che effettua il logout
def logout_view(request):
    logout(request)
    return  redirect('home')

#view per la registrazione prende i dati dal form e effettua il salvataggio
def registerPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Esegui altre operazioni dopo il salvataggio
            return  render(request, 'successoRegistrazione.html')  
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'register.html', context)


def accetta_rifiuta_view(request, richiesta_id, risultato):
    azione = risultato.lower()
    richiesta = RichiestaAdozione.objects.get(pk=richiesta_id)
    ID_animale = int(richiesta.animale.ID_animale)
    animale = Animale.objects.get(pk=ID_animale)

    if azione == 'true':
        # Esegui l'azione di accettazione 
        richiesta.richiesta = 'Accettata'
        richiesta.save()

        # Elimina l'animale
        animale.delete()

        return redirect('success_page_for_acceptance')
    else:
        # Esegui l'azione di rifiuto 
        richiesta.delete()

        return redirect('success_page_for_rejection')

def accetta_success(request):
    return render(request, 'accetta_richiesta.html')

def rifiuta_success(request):
    return render(request, 'rifiuta_richiesta.html')