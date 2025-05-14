from django.contrib import admin
from django.urls import path, include
from materias.views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('materias/', include('materias.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('', home, name='home'),
]
