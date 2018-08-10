# Importamos librerias
from django.conf.urls import url, include
from django.urls import path
from dolar import views


urlpatterns = [
    url(r'^clp$', views.dolar_a_clp),
    url(r'^usd$', views.clp_a_dolar),
    url(r'^populate_db$', views.populate_db),
]
