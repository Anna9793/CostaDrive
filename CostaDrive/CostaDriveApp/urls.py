from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth & Signup
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('login-redirect/', views.login_redirect, name='login_redirect'),
    path('signup/', views.client_signup, name='signup'),

    # Client Portal
    path('mi-cuenta/', views.client_dashboard, name='client_dashboard'),
    path('mi-cuenta/reservas/nueva/', views.client_crear_reserva, name='client_crear_reserva'),
    path('mi-cuenta/facturas/pagar/<int:id_factura>/', views.client_pagar_factura, name='client_pagar_factura'),

    # Staff Dashboard / Reservas
    path('', views.dashboard_reservas, name='dashboard'),
    path('reservas/nueva/', views.crear_reserva, name='crear_reserva'),
    path('reservas/editar/<int:id_reserva>/', views.modificar_reserva, name='editar_reserva'),
    path('reservas/cancelar/<int:id_reserva>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('reservas/facturar/<int:id_reserva>/', views.formalizar_reserva, name='formalizar_reserva'),
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('clientes/', views.listar_clientes, name='listar_clientes'),

    # Vehiculos
    path('vehiculos/', views.listar_vehiculos, name='listar_vehiculos'),
    path('vehiculos/mantenimiento/', views.registrar_mantenimiento, name='registrar_mantenimiento'),
    path('vehiculos/liberar/<int:id_vehiculo>/', views.liberar_vehiculo, name='liberar_vehiculo'),

    # Pagos y facturas
    path('facturas/', views.listar_facturas, name='listar_facturas'),
    path('facturas/pagar/<int:id_factura>/', views.pagar_factura, name='pagar_factura'),

    # Incidencias
    path('incidencias/', views.gestionar_incidencias, name='gestionar_incidencias'),
    path('incidencias/resolver/<int:id_incidencia>/', views.resolver_incidencia, name='resolver_incidencia'),
]