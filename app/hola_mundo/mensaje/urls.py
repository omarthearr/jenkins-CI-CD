from django.urls import path
from . import views

urlpatterns = [
    path('hola', views.hola),
    path('calificaciones', views.calificaciones),
    path('tabla/<int:numero>/<int:numero2>', views.tabla),
    path('calculadora/', views.calculadora),
]