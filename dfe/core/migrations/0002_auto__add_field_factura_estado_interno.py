# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Factura.estado_interno'
        db.add_column(u'core_factura', 'estado_interno',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Factura.estado_interno'
        db.delete_column(u'core_factura', 'estado_interno')


    models = {
        u'core.cliente': {
            'Meta': {'object_name': 'Cliente'},
            'codigo_iibb': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'codigo_postal': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'condicion_iva': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'domicilio': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'localidad': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'numero_documento': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'provincia': ('django.db.models.fields.IntegerField', [], {}),
            'razon_social': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'tipo_documento': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.comprobanteasociado': {
            'Meta': {'object_name': 'ComprobanteAsociado'},
            'factura': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comprobantes_asociados'", 'to': u"orm['core.Factura']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero_comprobante': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'punto_venta': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'tipo_comprobante': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.factura': {
            'Meta': {'object_name': 'Factura'},
            'cae': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'concepto': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'estado_interno': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'fecha_comprobante': ('django.db.models.fields.DateField', [], {}),
            'fecha_servicio_desde': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'fecha_servicio_hasta': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'fecha_vto_pago': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'forma_pago': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importe_iva': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '3'}),
            'importe_neto': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '3'}),
            'importe_op_exentas': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '3'}),
            'importe_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '3'}),
            'importe_total_conceptos': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '3'}),
            'importe_tributos': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '3'}),
            'moneda_cotizacion': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '4', 'decimal_places': '3'}),
            'moneda_id': ('django.db.models.fields.CharField', [], {'default': "'PES'", 'max_length': '3'}),
            'motivo': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'numero_cbte_desde': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'numero_cbte_hasta': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'numero_documento': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'observaciones': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'punto_venta': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'reproceso': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'resultado': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'tipo_comprobante': ('django.db.models.fields.IntegerField', [], {}),
            'tipo_documento': ('django.db.models.fields.IntegerField', [], {}),
            'vencimiento': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'core.itemfactura': {
            'Meta': {'object_name': 'ItemFactura'},
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'codigo': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'factura': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['core.Factura']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iva': ('django.db.models.fields.IntegerField', [], {}),
            'precio': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '3'}),
            'unidad': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.olicuotaivafactura': {
            'Meta': {'object_name': 'OlicuotaIVAFactura'},
            'base_imponible': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '3'}),
            'factura': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'olicuotas_iva'", 'to': u"orm['core.Factura']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importe_iva': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '3'}),
            'olicuota_iva': ('django.db.models.fields.IntegerField', [], {}),
            'olicuota_iva_valor': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '3'})
        },
        u'core.puntoventa': {
            'Meta': {'object_name': 'PuntoVenta'},
            'codigo_postal': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'domicilio': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'numero': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'core.tributofactura': {
            'Meta': {'object_name': 'TributoFactura'},
            'alicuota': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '3'}),
            'base_imponible': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '3'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'factura': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tributos'", 'to': u"orm['core.Factura']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importe': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '3'}),
            'tributo': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['core']