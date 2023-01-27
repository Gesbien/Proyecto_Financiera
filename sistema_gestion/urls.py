from django.urls import path
from . import views
from . import personas

urlpatterns = [
    path('',views.inicio,name='inicio'),
    path('personas',personas.index,name='principal'),
    path('personas/crear',personas.create,name='crear'),
    path('personas/editar',personas.edit,name='editar'),
    path('personas/eliminar',personas.delete,name='eliminar'),

]