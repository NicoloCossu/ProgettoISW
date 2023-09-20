"""
URL configuration for ProgettoISW project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from adozione import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/", views.home, name="home"),
    path('lista_animaliAmministratore/', views.lista_animaliAmministratore, name = 'lista_animaliAmministratore'),
    path("home_amministratore/", views.home_amministratore, name="home_amministratore"),
    path('register/',views.registerPage, name='register'),
    path('',auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('adotta/<int:animale_id>/', views.adotta, name='adotta'),
    path('modifica_animale/<int:animale_id>/', views.modifica_animale, name='modifica_animale'),
    path('accetta_rifiuta_view/<int:richiesta_id>/<str:risultato>/', views.accetta_rifiuta_view, name='accetta_rifiuta_view'),
    path('aggiungiAnimale/', views.aggiungiAnimale, name = 'aggiungiAnimale')
]