from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import Animale
from .forms import RichiestaAdozioneForm

def home(request):
    animali = Animale.objects.all() 
    return render(request, "home.html",{'animali':animali})
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

