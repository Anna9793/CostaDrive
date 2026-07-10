from django.contrib import admin

from .models import Reservas, Incidencias, Vehiculos, Clientes

@admin.register(Reservas)
class ReservasAdmin(admin.ModelAdmin):
    list_display = ('id_reserva', 'id_cliente', 'id_vehiculo', 'fecha_inicio', 'estado_reserva')
    list_filter = ('estado_reserva', 'fecha_inicio')
    search_fields = ('id_reserva', 'id_cliente__nombre', 'id_cliente__dni')
    ordering = ('-fecha_reserva',)

@admin.register(Incidencias)
class IncidenciasAdmin(admin.ModelAdmin):
    list_display = ('id_incidencia', 'id_reserva', 'fecha_incidencia', 'coste', 'estado_incidencia', 'destino_coste')
    list_filter = ('estado_incidencia', 'destino_coste', 'fecha_incidencia')
    search_fields = ('id_incidencia', 'descripcion')
    list_editable = ('estado_incidencia', 'destino_coste')

@admin.register(Vehiculos)
class VehiculosAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'marca', 'modelo', 'estado_vehiculo', 'precio_dia')
    list_filter = ('estado_vehiculo', 'marca')
    search_fields = ('matricula', 'marca', 'modelo')

@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'dni', 'telefono')
    search_fields = ('nombre', 'apellidos', 'dni', 'email')
