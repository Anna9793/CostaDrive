import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CostaDrive.settings')
django.setup()

from CostaDriveApp.models import Reservas
def listar_reservas():
    reservas_activas = Reservas.objects.filter(estado_reserva='ACTIVA')

    if not reservas_activas:
        print("No hay reservas activas en este momento.")
        return

    for r in reservas_activas:
        marca = r.id_vehiculo.marca
        modelo = r.id_vehiculo.modelo
        print(f"Reserva {r.id_reserva}: Vehículo {marca} {modelo}")

if __name__ == "__main__":
    listar_reservas()