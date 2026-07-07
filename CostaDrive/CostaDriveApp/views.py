from django.shortcuts import render, HttpResponse
from .db_utils import crear_reserva_db
from .forms import ReservaForm


def procesar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            try:
                crear_reserva_db(
                    form.cleaned_data['id_cliente'],
                    form.cleaned_data['id_vehiculo'],
                    form.cleaned_data['fecha_inicio'],
                    form.cleaned_data['fecha_fin']
                )
                return HttpResponse("¡Reserva creada con éxito!")
            except Exception as e:
                return HttpResponse(f"Error en Oracle: {e}")

    else:
        form = ReservaForm()
    
    return render(request, 'reserva_form.html', {'form': form}) 

def formalizar_reserva(request, id_reserva):
    try:
        generar_factura_db(id_reserva)
        return HttpResponse("Reserva creada y factura generada con éxito.")
    except Exception as e:
        return HttpResponse(f"Error: {e}")

