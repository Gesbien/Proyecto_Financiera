from django.urls import path
from sistema_gestion import views

urlpatterns = [
    path('',views.index,name='index')
]