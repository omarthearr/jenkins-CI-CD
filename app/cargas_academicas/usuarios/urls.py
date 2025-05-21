from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('datos-alumno', views.nuevo_alumno, name='datos_alumno'),
    path('obtener-programas/<int:id>',
         views.obtener_programas, name='obtener_programas'),

    path('', views.lista_usuarios, name='lista_usuarios'),
    path('registro-usuario', views.nuevo_usuario, name='nuevo_usuario'),
    path('activar/<slug:uidb64>/<slug:token>',
         views.ActivarCuenta.as_view(), name='activar'),

]
