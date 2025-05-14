from django.urls import path
from . import views


urlpatterns = [
    path('lista-unidades', views.lista_unidades, name='lista_unidades'),
    path('nueva-unidad', views.nueva_unidad, name='nueva_unidad'),
    path('eliminar-unidad/<int:id>', views.eliminar_unidad, name='eliminar_unidad'),
    path('editar-unidad/<int:id>', views.editar_unidad, name='editar_unidad'),
    

    path('lista-programas', views.ProgramasListView.as_view(), name='lista_programas'),
    path('lista-programas-filter', views.lista_programas_filter, name='lista_programas_filter'),
    
    path('nuevo-programa', views.ProgramaCreateView.as_view(), name='nuevo_programa'),
    path('editar-programa/<int:pk>', views.ProgramaUpdateView.as_view(), name='editar_programa'),
    path('eliminar-programa/<int:pk>', views.ProgramaDeleteView.as_view(), name='eliminar_programa'),
    


    # path('lista/', views.lista, name='lista_materias'),
    # path('nueva/', views.nueva, name='nueva_materia'),
    # path('eliminar/<str:clave>', views.eliminar, name='eliminar_materia'),

]
