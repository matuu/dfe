# -*- coding: utf-8 -*-
from collections import defaultdict
from decimal import Decimal
from django.db import models

from .parametros_afip import (
    CONCEPTO, TIPO_DOCUMENTO, TIPO_COMPROBANTE, MONEDA, FORMA_PAGO, PROVINCIA,
    ALICUOTA_IVA, UNIDAD, TIPO_ATRIBUTO)


class Cliente(models.Model):
    """
    Representa un cliente, puede ser una persona física o jurídica.

    """
    razon_social = models.CharField(u"Razón Social", max_length=200)
    tipo_documento = models.IntegerField(u"Tipo de Documento", choices=TIPO_DOCUMENTO)
    numero_documento = models.CharField(u"Número de documento", max_length=15)
    condicion_iva = models.IntegerField(u"Categoría IVA", max_length=2)
    domicilio = models.CharField(u"Domicilio", max_length=200)
    # Desconozco código IIBB, seguro está nomenclado
    codigo_iibb = models.CharField(u"Código IIBB", max_length=200)
    telefono = models.CharField(u"Teléfono", max_length=200, blank=True)
    localidad = models.CharField(u"Localidad", max_length=200)
    provincia = models.IntegerField(u"Provincia", choices=PROVINCIA)
    codigo_postal = models.CharField(u"Código postal", max_length=200)
    email = models.EmailField(u"Correo electrónico", blank=True)

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __unicode__(self):
        return u"{} ({})".format(
            self.razon_social,
            self.numero_documento
        )


class PuntoVenta(models.Model):
    """
    Un punto de venta autorizado en la AFIP.

    """
    domicilio = models.CharField(u"Domicilio", max_length=200)
    telefono = models.CharField(u"Teléfono", max_length=200)
    codigo_postal = models.CharField(u"Código postal", max_length=200)
    nombre = models.CharField(u"Nombre", max_length=200)
    # número de punto de venta registrado en AFIP
    numero = models.IntegerField(u"Número AFIP", max_length=4)

    class Meta:
        verbose_name = "punto de venta"
        verbose_name_plural = "puntos de venta"

    def __unicode__(self):
        return unicode(self.numero)


class Factura(models.Model):
    """ Representa una factura, con servicios y/o productos facturados.

    """
    ESTADO_INTERNO = ((1, 'Inicial'),
                      (2, 'Informada y aceptada'),
                      (3, 'Informada y rechazada'),
                      (4, 'Error'),)

    # Tipo (80 CUIT, 96 DNI, etc. según tabla de parámetros de AFIP)
    tipo_documento = models.IntegerField(u"Tipo de Documento", choices=TIPO_DOCUMENTO)

    # Número de Documento del cliente (receptor de la factura).
    # Usar tipo_doc=99 y nro_doc=0 para consumidores finales (Factura B < $1000)
    numero_documento = models.CharField(u"Número de documento", max_length=15)
    tipo_comprobante = models.IntegerField(u"Tipo de comprobante", choices=TIPO_COMPROBANTE)
    # debe estar autorizado para WSFE
    punto_venta = models.IntegerField(u"Punto de venta", max_length=2)  # 0 - 99
    # Nros de comprobante, el mismo si es factura individual
    numero_cbte_desde = models.CharField(u"N° de comprobante desde", max_length=20,
                                         help_text=u"Dejar vacio para asignar el siguiente automáticamente.")
    numero_cbte_hasta = models.CharField(u"N° de comprobante hasta", max_length=20,
                                         help_text=u"Dejar vacio para asignar el siguiente automáticamente.")
    # Fecha del comprobante (no puede ser mayor o menor a 10 días)
    fecha_comprobante = models.DateField(u"Fecha")
    concepto = models.IntegerField(u"Concepto", default=3, choices=CONCEPTO)
    forma_pago = models.IntegerField(u"Forma de pago", choices=FORMA_PAGO)
    # Importe total de la factura (debe ser igual a la suma de
    # imp_total_conceptos + imp_op_exentas + importe_neto + importe_iva + importe_tributos)
    importe_total = models.DecimalField(u"Importe Total", max_digits=18, decimal_places=3)
    # Importe total de conceptos no gravados por el IVA
    importe_total_conceptos = models.DecimalField(
        u"Importe total de conceptos no gravados", max_digits=18, decimal_places=3)
    # Importe neto (gravado por el IVA) de la factura (igual a la suma de base_imponible para todas las alicuotas)
    importe_neto = models.DecimalField(u"Importe neto", max_digits=18, decimal_places=3)
    # Importe del IVA liquidado (igual a la suma de importe_iva para todas las alícuotas)
    importe_iva = models.DecimalField(u"Importe IVA", max_digits=18, decimal_places=3)
    # Importe de otros tributos (incluyendo percepciones de IVA, retenciones, IVA no inscripto, etc.)
    importe_tributos = models.DecimalField(
        u"Importe de otros tributos", max_digits=18, decimal_places=3)
    # Importe de operaciones exentas
    importe_op_exentas = models.DecimalField(
        u"Importe de operaciones exentas", max_digits=18, decimal_places=3)
    moneda_id = models.CharField(u"Moneda", max_length=3, default='PES', choices=MONEDA)
    # Cotización de la moneda de la factura (actualmente solo 1.00)
    moneda_cotizacion = models.DecimalField("Cotización de moneda", default=1, max_digits=4, decimal_places=3,
                                            help_text=u"Actualmente, sólo se acepta el valor 1.")
    # Fecha de vencimiento de pago (si es de servicios)
    fecha_vto_pago = models.DateField(u"Fecha de vencimiento de pago", null=True,
                                      help_text=u"Completar sólo si se informan servicios.")
    fecha_servicio_desde = models.DateField(u"Fecha de servicio (inicio)", null=True,
                                            help_text=u"Completar sólo si se informan servicios.")
    fecha_servicio_hasta = models.DateField(u"Fecha de servicio (fin)", null=True,
                                            help_text=u"Completar sólo si se informan servicios.")
    estado_interno = models.IntegerField(u"Estado", default=1, choices=ESTADO_INTERNO)

    # Datos de resultado (luego de obtener el CAE)
    observaciones = models.CharField(u"Observaciones AFIP", max_length=512, blank=True, null=True,
                                     help_text=u"No completar. Será informado por la AFIP.")
    resultado = models.CharField(u"Resultado AFIP", max_length=20, null=True, blank=True,
                                 help_text=u"No completar. Será informado por la AFIP.")
    vencimiento = models.CharField(u"Vencimiento informado", max_length=20, null=True, blank=True,
                                   help_text=u"No completar. Será informado por la AFIP.")
    motivo = models.CharField(u"Motivo AFIP", max_length=20, null=True, blank=True,
                              help_text=u"No completar. Será informado por la AFIP.")
    cae = models.CharField(u"CAE", max_length=20, null=True, blank=True,
                           help_text=u"No completar. Será informado por la AFIP.")
    reproceso = models.CharField(u"Reproceso", max_length=20, null=True, blank=True,
                                 help_text=u"No completar. Será informado por la AFIP.")

    class Meta:
        verbose_name = "factura"
        verbose_name_plural = "facturas"

    def __unicode__(self):
        if self.numero_cbte_desde == self.numero_cbte_hasta:
            return u"{}-{}".format(
                self.punto_venta,
                self.numero_cbte_desde)
        else:
            return u"{}-{} | {}-{}".format(
                self.punto_venta,
                self.numero_cbte_desde,
                self.punto_venta,
                self.numero_cbte_hasta)

    def recalcular(self):
        """
        Al llamar a este método, se vuelven a calcular los totales de la factura,
        recorriendo los items de la factura y los tributos adicionales.
        Este método establece las alícuotas IVA a informar.

        """
        # recorro items
        total_neto = 0
        a_iva = defaultdict(Decimal)
        for item in self.items.all():
            total_neto += item.neto
            a_iva[item.iva] = a_iva[item.iva] + item.valor_iva  # acumulo el iva para cada alicuota
        for iva in a_iva:
            alicuota = AlicuotaIVAFactura()
            # TODO: asociar alicuotas ivas



class ItemFactura(models.Model):
    """
    Representa cada item de la factura.

    """
    factura = models.ForeignKey(Factura, verbose_name=u"Factura", related_name="items")
    descripcion = models.CharField(u"Descripción", max_length=400, null=True, blank=True)
    precio = models.DecimalField(u"Precio", max_digits=18, decimal_places=3)
    iva = models.IntegerField(u"Alícuota IVA", choices=ALICUOTA_IVA)
    cantidad = models.IntegerField(u"Cantidad")
    unidad = models.IntegerField(u"Unidad", choices=UNIDAD)
    codigo = models.CharField(max_length=400, null=True, blank=True)

    def __unicode__(self):
        return u"{}".format(
            str(self.id) if not self.descripcion else self.descripcion
        )

    class Meta:
        verbose_name = "Item de factura"
        verbose_name_plural = "Ítemes de factura"

    @property
    def neto(self):
        return self.precio * self.cantidad

    @property
    def valor_iva(self):
        return self.neto * Decimal(dict(ALICUOTA_IVA)[self.iva]) / 100



class AlicuotaIVAFactura(models.Model):
    """
    Representa cada alicuota IVA de la factura.

    """
    factura = models.ForeignKey(Factura, verbose_name=u"Factura", related_name="alicuotas_iva")
    alicuota_iva = models.IntegerField(u"Alícuota IVA", choices=ALICUOTA_IVA)
    # Además, guardo si valor decimal, por si cambian en algún momento
    alicuota_iva_valor = models.DecimalField(u"Valor Alícuota IVA", max_digits=18, decimal_places=3)
    base_imponible = models.DecimalField(u"Base imponible", max_digits=18, decimal_places=3)
    importe_iva = models.DecimalField(u"Importe liquidado", max_digits=18, decimal_places=3)

    def __unicode__(self):
        return u"{} ({}%)".format(
            self.base_imponible,
            ALICUOTA_IVA[self.olicuota_iva][1]
        )


class TributoFactura(models.Model):
    """
    Otros tributos que pueden ser incluidos en la factura.

    """
    factura = models.ForeignKey(Factura, verbose_name=u"Factura", related_name="tributos")
    tributo = models.IntegerField(u"Tributo", choices=TIPO_ATRIBUTO)
    descripcion = models.CharField(U"Descripción", max_length=400)
    base_imponible = models.DecimalField(u"Base imponible", max_digits=18, decimal_places=3)
    alicuota = models.DecimalField(u"Alícuota", max_digits=18, decimal_places=3)
    importe = models.DecimalField(u"Importe liquidado", max_digits=18, decimal_places=3)

    class Meta:
        verbose_name = "tributo"
        verbose_name_plural = "tributos"

    def __unicode__(self):
        return u"{} ({})".format(
            self.descripcion,
            TIPO_ATRIBUTO[self.tributo][1]
        )


class ComprobanteAsociado(models.Model):
    """
    A un comprobante del tipo Nota de crédito o Nota de débito, es posible añadirle
    la asociación de los comprobantes correspondientes.

    """
    factura = models.ForeignKey(
        Factura, verbose_name=u"Comprobante asociado", related_name="comprobantes_asociados")
    tipo_comprobante = models.IntegerField(u"Tipo de comprobante", choices=TIPO_COMPROBANTE)
    # debe estar autorizado para WSFE
    punto_venta = models.IntegerField(u"Punto de venta", max_length=2)  # 0 - 99
    numero_comprobante = models.CharField(u"N° de comprobante", max_length=20)

    class Meta:
        verbose_name = "comprobante asociado"
        verbose_name_plural = "comprobantes asociados"

    def __unicode__(self):
        return u"{}-{}".format(
            self.punto_venta,
            self.numero_comprobante
        )
