import json
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import group_required, db_action
from .api_utils import obtener_precios_carburante_alicante, obtener_tiempo_denia
from .db_utils import (
    crear_reserva_db,
    obtener_reservas_db,
    obtener_reserva_por_id_db,
    actualizar_fechas_reserva_db,
    contar_reservas_pendientes_db,
    cancelar_reserva_db,
    generar_factura_db,
    registrar_pago_db,
    obtener_vehiculos_db,
    obtener_facturas_db,
    obtener_factura_por_id_db,
    obtener_incidencias_db,
    obtener_mantenimientos_db,
    crear_incidencia_db,
    registrar_mantenimiento_db,
    liberar_vehiculo_mantenimiento_db,
    resolver_incidencia_db,
    crear_cliente_db,
    obtener_clientes_db,
    obtener_tendencia_mensual_db,
    obtener_distribucion_categorias_db
)
from django.contrib.auth.models import User, Group
from django.contrib.auth import login as auth_login
from .forms import (
    ReservaForm,
    ReservaUpdateForm,
    PagoForm,
    IncidenciaForm,
    VehiculoMantenimientoForm,
    ClienteForm,
    RegistroClienteForm,
    ClientReservaForm
)
from .models import Vehiculos, Reservas, Facturas, Incidencias, Clientes

@login_required
@group_required('Manager', 'Receptionist')
def dashboard_reservas(request):
    cliente_id = request.GET.get("cliente")
    
    # Quick Stats using ORM (unmanaged models)
    try:
        total_vehiculos = Vehiculos.objects.count()
        vehiculos_disponibles = Vehiculos.objects.filter(estado_vehiculo='DISPONIBLE').count()
        vehiculos_alquilados = Vehiculos.objects.filter(estado_vehiculo='ALQUILADO').count()
        vehiculos_mantenimiento = Vehiculos.objects.filter(estado_vehiculo='MANTENIMIENTO').count()
        total_reservas_activas = Reservas.objects.filter(estado_reserva='ACTIVA').count()
        incidencias_abiertas = Incidencias.objects.filter(estado_incidencia='ABIERTA').count()
    except Exception as e:
        total_vehiculos = vehiculos_disponibles = vehiculos_alquilados = vehiculos_mantenimiento = total_reservas_activas = incidencias_abiertas = 0
        messages.error(request, f"Error al cargar estadísticas de la base de datos: {e}")

    # Fetch chart data
    try:
        tendencia_mensual = obtener_tendencia_mensual_db()
        distribucion_cat = obtener_distribucion_categorias_db()

        tendencia_labels = [row[0] for row in tendencia_mensual]
        tendencia_valores = [row[1] for row in tendencia_mensual]

        cat_labels = [row[0] for row in distribucion_cat]
        cat_valores = [row[1] for row in distribucion_cat]
    except Exception as e:
        tendencia_labels = tendencia_valores = cat_labels = cat_valores = []
        messages.error(request, f"Error al cargar datos de gráficos: {e}")

    contexto = {
        'reservas': obtener_reservas_db(cliente_id),
        'pendientes': contar_reservas_pendientes_db(),
        'stats': {
            'total_vehiculos': total_vehiculos,
            'disponibles': vehiculos_disponibles,
            'alquilados': vehiculos_alquilados,
            'mantenimiento': vehiculos_mantenimiento,
            'reservas_activas': total_reservas_activas,
            'incidencias_abiertas': incidencias_abiertas,
        },
        'charts_data': {
            'tendencia_labels': json.dumps(tendencia_labels),
            'tendencia_valores': json.dumps(tendencia_valores),
            'cat_labels': json.dumps(cat_labels),
            'cat_valores': json.dumps(cat_valores),
        }
    }
    return render(request, 'dashboard.html', contexto)

@login_required
@group_required('Manager', 'Receptionist')
@db_action("Reserva creada con éxito.", fallback_url='dashboard')
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            crear_reserva_db(
                int(form.cleaned_data['cliente']),
                int(form.cleaned_data['vehiculo']),
                form.cleaned_data['fecha_inicio'],
                form.cleaned_data['fecha_fin']
            )
            return redirect('dashboard')
    else:
        cliente_id = request.GET.get('cliente')
        form = ReservaForm(initial={'cliente': cliente_id} if cliente_id else None)

    return render(request, 'reserva_form.html', {'form': form, 'editing': False})

@login_required
@group_required('Manager', 'Receptionist')
@db_action("Reserva actualizada con éxito.", fallback_url='dashboard')
def modificar_reserva(request, id_reserva):
    reserva = obtener_reserva_por_id_db(id_reserva)
    if not reserva:
        messages.error(request, "La reserva no existe.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ReservaUpdateForm(request.POST)
        if form.is_valid():
            actualizar_fechas_reserva_db(
                id_reserva,
                form.cleaned_data['fecha_inicio'],
                form.cleaned_data['fecha_fin']
            )
            return redirect('dashboard')
    else:
        fecha_ini = reserva[3]
        fecha_fn = reserva[4]
        initial_data = {
            'fecha_inicio': fecha_ini.strftime('%Y-%m-%d') if hasattr(fecha_ini, 'strftime') else fecha_ini,
            'fecha_fin': fecha_fn.strftime('%Y-%m-%d') if hasattr(fecha_fn, 'strftime') else fecha_fn
        }
        form = ReservaUpdateForm(initial=initial_data)

    return render(request, 'reserva_form.html', {'form': form, 'editing': True, 'reserva': reserva})

@login_required
@group_required('Manager', 'Receptionist')
@db_action("Reserva cancelada con éxito.", fallback_url='dashboard')
def cancelar_reserva(request, id_reserva):
    cancelar_reserva_db(id_reserva)
    return redirect('dashboard')

@login_required
@group_required('Manager', 'Receptionist')
@db_action("Factura generada correctamente.", fallback_url='dashboard')
def formalizar_reserva(request, id_reserva):
    generar_factura_db(id_reserva)
    return redirect('listar_facturas')

@login_required
def listar_vehiculos(request):
    vehiculos = obtener_vehiculos_db()
    return render(request, 'vehicles.html', {'vehiculos': vehiculos})

@login_required
@group_required('Manager', 'Maintenance')
@db_action("Vehículo enviado a mantenimiento correctamente.", fallback_url='listar_vehiculos')
def registrar_mantenimiento(request):
    if request.method == 'POST':
        form = VehiculoMantenimientoForm(request.POST)
        if form.is_valid():
            registrar_mantenimiento_db(
                int(form.cleaned_data['vehiculo']),
                form.cleaned_data['descripcion'],
                form.cleaned_data['coste']
            )
            return redirect('listar_vehiculos')
    else:
        form = VehiculoMantenimientoForm()

    return render(request, 'mantenimiento_form.html', {'form': form})

@login_required
@group_required('Manager', 'Maintenance')
@db_action("Vehículo devuelto al servicio activo correctamente.", fallback_url='listar_vehiculos')
def liberar_vehiculo(request, id_vehiculo):
    liberar_vehiculo_mantenimiento_db(id_vehiculo)
    return redirect('listar_vehiculos')

@login_required
@group_required('Manager', 'Receptionist')
def listar_facturas(request):
    facturas = obtener_facturas_db()
    return render(request, 'facturas.html', {'facturas': facturas})

@login_required
@group_required('Manager', 'Receptionist')
@db_action("Pago registrado con éxito.", fallback_url='listar_facturas')
def pagar_factura(request, id_factura):
    factura = obtener_factura_por_id_db(id_factura)
    if not factura:
        messages.error(request, "La factura no existe.")
        return redirect('listar_facturas')

    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            registrar_pago_db(
                id_factura,
                form.cleaned_data['metodo_pago'],
                form.cleaned_data['importe']
            )
            return redirect('listar_facturas')
    else:
        # Prepopulate remaining amount
        # factura format: (id_factura, id_reserva, fecha_factura, importe_total, estado_pago, ...)
        form = PagoForm(initial={'importe': factura[3]})

    return render(request, 'pagar_factura.html', {'form': form, 'factura': factura})

@login_required
@db_action("Incidencia registrada con éxito.", fallback_url='gestionar_incidencias')
def gestionar_incidencias(request):
    if request.method == 'POST':
        # Validar permisos de creación (Manager, Receptionist y Maintenance pueden registrar incidencias)
        form = IncidenciaForm(request.POST)
        if form.is_valid():
            crear_incidencia_db(
                int(form.cleaned_data['reserva']),
                form.cleaned_data['descripcion'],
                form.cleaned_data['coste'],
                form.cleaned_data['destino_coste']
            )
            return redirect('gestionar_incidencias')
    else:
        form = IncidenciaForm()

    incidencias = obtener_incidencias_db()
    mantenimientos = obtener_mantenimientos_db()

    contexto = {
        'form': form,
        'incidencias': incidencias,
        'mantenimientos': mantenimientos
    }
    return render(request, 'incidencias.html', contexto)

@login_required
@group_required('Manager', 'Maintenance')
@db_action("Incidencia resuelta con éxito.", fallback_url='gestionar_incidencias')
def resolver_incidencia(request, id_incidencia):
    if request.method == 'POST':
        coste_final = request.POST.get('coste_final', 0.00)
        resolver_incidencia_db(id_incidencia, float(coste_final))
    return redirect('gestionar_incidencias')

@login_required
@group_required('Manager', 'Receptionist')
@db_action(fallback_url='listar_clientes')
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            new_id = crear_cliente_db(
                form.cleaned_data['nombre'],
                form.cleaned_data['apellidos'],
                form.cleaned_data['dni'],
                form.cleaned_data['telefono'],
                form.cleaned_data['email']
            )
            messages.success(request, f"Cliente {form.cleaned_data['nombre']} {form.cleaned_data['apellidos']} registrado con éxito.")
            if new_id:
                new_id = int(new_id)
                return redirect(f'/app/reservas/nueva/?cliente={new_id}')
            return redirect('crear_reserva')
    else:
        form = ClienteForm()

    return render(request, 'cliente_form.html', {'form': form})

@login_required
def login_redirect(request):
    """Redirecciona al usuario a su página principal correspondiente según su rol."""
    if request.user.groups.filter(name='Client').exists():
        return redirect('client_dashboard')
    if request.user.groups.filter(name='Maintenance').exists():
        return redirect('listar_vehiculos')
    return redirect('dashboard')

@login_required
@group_required('Manager', 'Receptionist')
def listar_clientes(request):
    """Muestra un directorio de todos los clientes registrados."""
    clientes = obtener_clientes_db()
    return render(request, 'clientes.html', {'clientes': clientes})

def client_signup(request):
    if request.user.is_authenticated:
        return redirect('login_redirect')
        
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                nombre = form.cleaned_data['nombre']
                apellidos = form.cleaned_data['apellidos']
                dni = form.cleaned_data['dni']
                telefono = form.cleaned_data['telefono']
                
                # 1. Create Django user
                user = User.objects.create_user(username=email, email=email, password=password)
                user.first_name = nombre
                user.last_name = apellidos
                user.save()
                
                # 2. Add to Client group
                group = Group.objects.get(name='Client')
                user.groups.add(group)
                
                # 3. Insert into Oracle CLIENTES
                crear_cliente_db(nombre, apellidos, dni, telefono, email)
                
                # 4. Log in
                auth_login(request, user)
                
                messages.success(request, f"¡Bienvenido a CostaDrive, {nombre}! Tu cuenta ha sido creada con éxito.")
                return redirect('login_redirect')
            except Exception as e:
                messages.error(request, f"Error al procesar el registro: {e}")
    else:
        form = RegistroClienteForm()
        
    return render(request, 'signup.html', {'form': form})

@login_required
@group_required('Client')
def client_dashboard(request):
    cliente = Clientes.objects.filter(email=request.user.email).first()
    if not cliente:
        messages.error(request, "Tu cuenta no está asociada a ningún cliente.")
        return redirect('logout') # Logout if inconsistent state
        
    reservas = obtener_reservas_db(cliente.id_cliente)
    
    # Fetch third-party API data for client value-add
    fuel_stats = obtener_precios_carburante_alicante()
    weather_stats = obtener_tiempo_denia()
    
    contexto = {
        'reservas': reservas,
        'cliente': cliente,
        'fuel_stats': fuel_stats,
        'weather_stats': weather_stats
    }
    return render(request, 'client_dashboard.html', contexto)

@login_required
@group_required('Client')
@db_action("¡Tu reserva ha sido creada con éxito!", fallback_url='client_dashboard')
def client_crear_reserva(request):
    cliente = Clientes.objects.filter(email=request.user.email).first()
    if not cliente:
        messages.error(request, "Tu cuenta no está asociada a ningún cliente.")
        return redirect('login_redirect')

    if request.method == 'POST':
        form = ClientReservaForm(request.POST)
        if form.is_valid():
            crear_reserva_db(
                int(cliente.id_cliente),
                int(form.cleaned_data['vehiculo']),
                form.cleaned_data['fecha_inicio'],
                form.cleaned_data['fecha_fin']
            )
            return redirect('client_dashboard')
    else:
        form = ClientReservaForm()

    return render(request, 'client_reserva_form.html', {'form': form})

@login_required
@group_required('Client')
@db_action(fallback_url='client_dashboard')
def client_pagar_factura(request, id_factura):
    cliente = Clientes.objects.filter(email=request.user.email).first()
    if not cliente:
        messages.error(request, "Tu cuenta no está asociada a ningún cliente.")
        return redirect('login_redirect')

    factura = obtener_factura_por_id_db(id_factura)
    if not factura:
        messages.error(request, "Factura no encontrada.")
        return redirect('client_dashboard')

    # Verify ownership
    from .db_utils import _ejecutar_sql
    reserva_info = _ejecutar_sql("SELECT id_cliente FROM RESERVAS WHERE id_reserva = %s", [factura[1]])
    if not reserva_info or int(reserva_info[0][0]) != int(cliente.id_cliente):
        messages.error(request, "Acceso denegado.")
        return redirect('client_dashboard')

    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            registrar_pago_db(
                int(id_factura),
                form.cleaned_data['metodo_pago'],
                form.cleaned_data['importe']
            )
            messages.success(request, f"¡Pago de {form.cleaned_data['importe']}€ registrado con éxito!")
            return redirect('client_dashboard')
    else:
        form = PagoForm(initial={'importe': factura[3]})

    return render(request, 'client_pagar_factura.html', {'form': form, 'factura': factura})
