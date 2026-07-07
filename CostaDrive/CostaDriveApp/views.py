from django.shortcuts import render
from .db_utils import crear_reserva_db
from django.http import HttpResponse

def procesar_reserva(request):
    if request.method == 'POST':

        try:
            crear_reserva_db(1, 6, '2026-08-01', '2026-08-08')
            return HttpResponse("¡Reserva creada con éxito en Oracle!")
        except Exception as e:
            return HttpResponse(f"Error al crear reserva: {e}")

    else:
        return HttpResponse("Este es el formulario. Proximamente verás aquí un HTML")

