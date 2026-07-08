from django.urls import path
from . import views

urlpatterns = [
    path('reservas/', views.dashboard_reservas, name='dashboard_reservas'),
    path('reservas/editar/<int_id>', views.crear_reserva, name ='crear_reserva'),
]