# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'frontend.views',
    url(r'^$', 'index', name='index'),
    url(r'^comprobante/nuevo$', 'comprobante_nuevo', name='comprobante_nuevo')
)