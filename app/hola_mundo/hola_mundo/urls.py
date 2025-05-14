from django.contrib import admin
from django.urls import path, include
from mensaje import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mensaje/', include('mensaje.urls')),
    path('', views.bienvenida),
]


'''
http://localhost:8000/mensaje/hola
https://ingosftware.uaz.edu.mx/hola
'''