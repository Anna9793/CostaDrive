from django.shortcuts import render, HttpResponse
from .db_utils import (crear_reserva_db,
                      obtener_reservas_db,
                      obtener_reservas_cliente_db,
                      contar_reservas_pendientes_db)
from .forms import ReservaForm

def dashboard_reservas(request):
    cliente_id = request.GET.get("cliente")
    contexto = {
        'reservas': obtener_reservas_db(cliente_id),
        'pendientes': contar_reservas_pendientes_db(),
    }
    return render(request, 'dashboard.html', contexto)

def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
                crear_reserva_db(
                    form.cleaned_data['id_cliente'],
                    form.cleaned_data['id_vehiculo'],
                    form.cleaned_data['fecha_inicio'],
                    form.cleaned_data['fecha_fin']
                )
                return redirect('dashboard')

    else:
        form = ReservaForm()

    return render(request, 'reserva_form.html', {'form': form})

def cancelar_reserva(request, id_reserva):
    

def modificar_reserva(request, id_reserva,)


def formalizar_reserva(request, id_reserva):
    try:
        generar_factura_db(id_reserva)
        return HttpResponse("Reserva creada y factura generada con éxito.")
    except Exception as e:
        return HttpResponse(f"Error: {e}")

