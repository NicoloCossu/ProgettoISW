from django.shortcuts import render

def home(request):
    animals= [
        {'specie':'ciao', 'razza': 'aaa', 'eta': 'tt','descrizione': 'd'},
        {'specie':'ciao2', 'razza': 'aaa', 'eta': 'tt','descrizione': 'd'},
        {'specie':'ciao3', 'razza': 'aaa', 'eta': 'tt','descrizione': 'd'},
    ]
    return render(request, "polls/home.html",{'animals':animals})