from datetime import date
from django import forms
from django.forms.formsets import formset_factory

from .models import Factura


class CreateComprobante(forms.ModelForm):
    fecha_comprobante = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
        initial=date.today())

    class Meta:
        model = Factura
        fields = (
            'tipo_documento', 'numero_documento', 'tipo_comprobante',
            'punto_venta', 'numero_cbte_desde', 'numero_cbte_hasta',
            'fecha_comprobante', 'concepto', 'forma_pago', 'importe_total',
            'importe_total_conceptos', 'importe_neto', 'importe_iva',
            'importe_tributos', )