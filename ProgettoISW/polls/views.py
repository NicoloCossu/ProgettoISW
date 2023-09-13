from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import Animale, RichiestaAdozione
from .forms import RichiestaAdozioneForm
from .filters import AnimalFilter
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
    context = {'richieste':richieste}
    return render(request,'home_amministratore.html',context)

def successo(request):
    return render(request, 'successo.html')


def invia_richiesta_adozione(request):
    if request.method == 'POST':
        form = RichiestaAdozioneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('successo/')  # Redirigi a una pagina di successo
    else:
        form = RichiestaAdozioneForm()
    return render(request, 'adotta.html', {'form': form})


def registerPage(request):
    form= UserCreationForm()
    if request.method == 'POST':
        form= UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    context={'form':form}
    return render(request, 'register.html',context)

