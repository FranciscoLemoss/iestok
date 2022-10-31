from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("cadastro/", views.cadastro, name='cadastro'),
    path("login/", views.login, name='login'),
    path("congratulations/", views.congratulations, name='congratulations'),
    path("sair/", views.sair, name='sair'),
]