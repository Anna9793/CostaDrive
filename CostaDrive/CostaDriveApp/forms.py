from django import forms
from .models import Clientes, Vehiculos, Reservas

class ReservaForm(forms.Form):
    cliente = forms.ChoiceField(label="Cliente", widget=forms.Select(attrs={'class': 'form-select'}))
    vehiculo = forms.ChoiceField(label="Vehículo", widget=forms.Select(attrs={'class': 'form-select'}))
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically load clients
        try:
            clientes = Clientes.objects.all().order_by('nombre', 'apellidos')
            self.fields['cliente'].choices = [
                (c.id_cliente, f"{c.nombre} {c.apellidos} ({c.dni})") for c in clientes
            ]
        except Exception:
            self.fields['cliente'].choices = []

        # Dynamically load available vehicles
        try:
            vehiculos = Vehiculos.objects.filter(estado_vehiculo='DISPONIBLE').order_by('marca', 'modelo')
            self.fields['vehiculo'].choices = [
                (v.id_vehiculo, f"{v.marca} {v.modelo} ({v.matricula}) - {v.precio_dia}€/día") for v in vehiculos
            ]
        except Exception:
            self.fields['vehiculo'].choices = []

class ReservaUpdateForm(forms.Form):
    fecha_inicio = forms.DateField(label="Fecha de Inicio", widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    fecha_fin = forms.DateField(label="Fecha de Fin", widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

class PagoForm(forms.Form):
    metodo_pago = forms.ChoiceField(
        label="Método de Pago",
        choices=[
            ('TARJETA', 'Tarjeta'),
            ('EFECTIVO', 'Efectivo'),
            ('TRANSFERENCIA', 'Transferencia')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    importe = forms.DecimalField(label="Importe (€)", max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))

class IncidenciaForm(forms.Form):
    reserva = forms.ChoiceField(label="Reserva Asociada", widget=forms.Select(attrs={'class': 'form-select'}))
    descripcion = forms.CharField(label="Descripción de la Incidencia", widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}))
    coste = forms.DecimalField(label="Coste Estimado (€)", max_digits=10, decimal_places=2, initial=0.00, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))
    destino_coste = forms.ChoiceField(
        label="Destino del Coste",
        choices=[
            ('EMPRESA', 'Empresa (Mantenimiento)'),
            ('CLIENTE', 'Cliente (Facturación adicional)'),
            ('SEGURO', 'Seguro')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            reservas = Reservas.objects.exclude(estado_reserva='CANCELADA').order_by('-id_reserva')
            self.fields['reserva'].choices = [
                (r.id_reserva, f"Reserva {int(r.id_reserva)} - Cliente: {r.id_cliente.nombre} {r.id_cliente.apellidos} - Vehículo: {r.id_vehiculo.marca} {r.id_vehiculo.modelo}") for r in reservas
            ]
        except Exception:
            self.fields['reserva'].choices = []

class VehiculoMantenimientoForm(forms.Form):
    vehiculo = forms.ChoiceField(label="Vehículo", widget=forms.Select(attrs={'class': 'form-select'}))
    descripcion = forms.CharField(label="Motivo del Mantenimiento", widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}))
    coste = forms.DecimalField(label="Coste (€)", max_digits=10, decimal_places=2, initial=0.00, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            vehiculos = Vehiculos.objects.exclude(estado_vehiculo='MANTENIMIENTO').order_by('marca', 'modelo')
            self.fields['vehiculo'].choices = [
                (v.id_vehiculo, f"{v.marca} {v.modelo} ({v.matricula}) - {v.estado_vehiculo}") for v in vehiculos
            ]
        except Exception:
            self.fields['vehiculo'].choices = []

class ClienteForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan'}))
    apellidos = forms.CharField(label="Apellidos", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Pérez Gómez'}))
    dni = forms.CharField(label="DNI / NIE", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 12345678Z'}))
    telefono = forms.CharField(label="Teléfono", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. +34 600 123 456'}))
    email = forms.EmailField(label="Correo Electrónico", max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ej. juan.perez@example.com'}))

class RegistroClienteForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan'}))
    apellidos = forms.CharField(label="Apellidos", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Pérez Gómez'}))
    dni = forms.CharField(label="DNI / NIE", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 12345678Z'}))
    telefono = forms.CharField(label="Teléfono", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. +34 600 123 456'}))
    email = forms.EmailField(label="Correo Electrónico", max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ej. juan.perez@example.com'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'}))

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        # Check in Django auth User
        from django.contrib.auth.models import User
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        # Check in Oracle Clientes
        if Clientes.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado en la base de datos de clientes.")
        return email

    def clean_dni(self):
        dni = self.cleaned_data.get('dni').upper()
        if Clientes.objects.filter(dni=dni).exists():
            raise forms.ValidationError("Este DNI/NIE ya está registrado.")
        return dni

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        return password

class ClientReservaForm(forms.Form):
    vehiculo = forms.ChoiceField(label="Vehículo", widget=forms.Select(attrs={'class': 'form-select'}))
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically load available vehicles
        try:
            vehiculos = Vehiculos.objects.filter(estado_vehiculo='DISPONIBLE').order_by('marca', 'modelo')
            self.fields['vehiculo'].choices = [
                (v.id_vehiculo, f"{v.marca} {v.modelo} ({v.matricula}) - {v.precio_dia}€/día") for v in vehiculos
            ]
        except Exception:
            self.fields['vehiculo'].choices = []