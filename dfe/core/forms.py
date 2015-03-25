# -*- coding: utf-8 -*-
from datetime import date, timedelta
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.forms.formsets import formset_factory

from .models import Factura, ItemFactura, TributoFactura, ComprobanteAsociado
from .parametros_afip import (
    CONCEPTO, TIPO_DOCUMENTO, TIPO_COMPROBANTE, MONEDA, FORMA_PAGO, PROVINCIA,
    ALICUOTA_IVA, UNIDAD, TIPO_ATRIBUTO)

class DatepickerField(forms.DateField):
    u"""
    Un field del tipo fecha en el cual se utilizará
    el componente datepicker.

    """
    def __init__(self, *args, **kwargs):
        super(DatepickerField, self).__init__(*args, **kwargs)
        self.widget = forms.DateInput(attrs={'class': 'datepicker'})
        self.initial = date.today()


class CreateComprobante(forms.ModelForm):
    fecha_comprobante = DatepickerField()
    fecha_vto_pago = DatepickerField()
    fecha_servicio_desde = DatepickerField()
    fecha_servicio_hasta = DatepickerField()

    class Meta:
        model = Factura
        fields = (
            'tipo_documento', 'numero_documento', 'tipo_comprobante',
            'punto_venta', 'numero_cbte_desde', 'numero_cbte_hasta',
            'fecha_comprobante', 'concepto', 'forma_pago',
            'importe_total', 'importe_total_conceptos', 'importe_neto',
            'importe_iva', 'importe_tributos', 'importe_op_exentas',
            'fecha_vto_pago', 'fecha_servicio_desde', 'fecha_servicio_hasta')

    def clean(self):
        data = self.cleaned_data
        if data["concepto"] != 1:
            for fecha_servicio in ["fecha_vto_pago", "fecha_servicio_desde", "fecha_servicio_hasta", ]:

                if fecha_servicio not in data or data[fecha_servicio] is None:
                    raise ValidationError("Las fechas de servicio son obligatorias si se está declarando un servicio.")
        return data

    def clean_fecha_comprobante(self):
        fecha = self.cleaned_data["fecha_comprobante"]
        hoy = date.today()
        margen = timedelta(days=10)
        if not hoy - margen <= fecha <= hoy + margen:
            raise ValidationError("La fecha del comprobante debe estar en el rango de los 10 días.")
        return fecha


class CreateItemFacturaForm(forms.ModelForm):

    class Meta:
        model = ItemFactura
        fields = ('codigo', 'descripcion', 'cantidad', 'unidad',
                  'iva', 'precio', )

    def clean(self):
        data = self.cleaned_data
        for it in ['precio', 'cantidad', ]:
            if it in data and data[it] < 0:
                raise ValidationError(
                    "El valor de '{}' no puede ser negativo".format(it),
                    code='invalid',
                    params=data[it])
        return data


class CreateTributoFacturaForm(forms.ModelForm):

    class Meta:
        model = TributoFactura
        fields = ('tributo', 'descripcion', 'base_imponible', 'alicuota',
                  'importe', )

    def clean_importe(self):
        data = self.cleaned_data
        if data["importe"] != data["base_imponible"] * (data["alicuota"] / 100):
            raise ValidationError("Error en el cálculo del importe.")
        return data["importe"]


class CreateComprobanteAsociadoForm(forms.ModelForm):

    class Meta:
        model = ComprobanteAsociado
        fields = ('tipo_comprobante', 'punto_venta', 'numero_comprobante', )