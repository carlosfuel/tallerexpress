from django import forms
from .models import OrdenServicio


class OrdenServicioForm(forms.ModelForm):
    class Meta:
        model = OrdenServicio
        # numero_orden y las fechas NO van: son automáticos
        fields = ['cliente', 'vehiculo', 'mecanico', 'descripcion_problema', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'vehiculo': forms.Select(attrs={'class': 'form-select'}),
            'mecanico': forms.Select(attrs={'class': 'form-select'}),
            'descripcion_problema': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'descripcion_problema': 'Descripción del problema',
        }

    def clean(self):
        cleaned = super().clean()
        cliente = cleaned.get('cliente')
        vehiculo = cleaned.get('vehiculo')
        # Regla de negocio: el vehículo debe pertenecer al cliente elegido
        if cliente and vehiculo and vehiculo.cliente_id != cliente.id:
            raise forms.ValidationError(
                'El vehículo seleccionado no pertenece al cliente seleccionado.')
        return cleaned
