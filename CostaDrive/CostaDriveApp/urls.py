from django.urls import path
from . import views

urlpatterns = [
    path('crear-reserva/', views.procesar_reserva, name ='procesar_reserva'),
]