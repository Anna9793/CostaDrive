from django import forms

class ReservaForm(forms.Form):
    id_cliente = forms.IntegerField(label="ID Cliente")
    id_vehiculo = forms.IntegerField(label='ID Vehículo')
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))