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

from polls import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/", views.home, name="home"),
    path('home_amministratore/', views.homeAmministratore, name='home_amministratore'),
    path('register/',views.registerPage, name='register'),
    path('',auth_views.LoginView.as_view(), name='login'),
    path('adotta/',views.invia_richiesta_adozione, name='adotta'),
    path('adotta/successo/',views.successo, name='successo')
]