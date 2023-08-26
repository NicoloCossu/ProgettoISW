from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def home(request):
    animals= [
        {'specie':'ciao', 'razza': 'aaa', 'eta': 'tt','descrizione': 'd'},
        {'specie':'ciao2', 'razza': 'aaa', 'eta': 'tt','descrizione': 'd'},
        {'specie':'ciao3', 'razza': 'aaa', 'eta': 'tt','descrizione': 'd'},
    ]
    return render(request, "home.html",{'animals':animals})


def registerPage(request):
    form= UserCreationForm()

    if request.method == 'POST':
        form= UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    context={'form':form}
    return render(request, 'register.html',context)

def loginPage(request):
    context={}
    return render(request, 'login.html',context)