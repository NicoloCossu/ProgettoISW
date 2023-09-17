from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User  # Assicurati di importare il modello User
from .models import Animale, RichiestaAdozione
from .forms import RichiestaAdozioneForm
from .filters import AnimalFilter, RichesteFilter
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: not u.is_superuser, login_url='home_amministratore')
def home(request):
    animali = Animale.objects.all() 

    myFilter = AnimalFilter(request.GET, queryset=animali)
    animali = myFilter.qs

    context = {'animali': animali, 'myFilter': myFilter}
    return render(request, "home.html", context)



@user_passes_test(lambda u: u.is_superuser, login_url='home')
def homeAmministratore(request):
    richieste = RichiestaAdozione.objects.all()

    myFilter = RichesteFilter(request.GET, queryset=richieste)
    richieste = myFilter.qs

    context = {'richieste':richieste, 'myFilter': myFilter}
    return render(request,'home_amministratore.html',context)



#invio della richiesta di adozione prendendo l'id dell'animale selezionato e lo user loggato al momento dell'invio della richiesta
def adotta(request, animale_id):
    animale = Animale.objects.get(pk=animale_id)

    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data['animale'] = animale.ID_animale  
        form_data['user'] = request.user 
        form = RichiestaAdozioneForm(form_data)
        if form.is_valid():
            richiesta_adozione = form.save(commit=False)
            richiesta_adozione.animale = animale
            richiesta_adozione.utente = request.user
            richiesta_adozione.save()        
            return render(request, 'successoRegistrazione.html')
    else:
        form = RichiestaAdozioneForm(initial={'animale': animale_id, 'utente': request.user})
    context = {'animale': animale, 'form': form}
    return render(request, 'adotta.html', context)


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

