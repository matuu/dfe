from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView

from enhanced_cbv.views.edit import InlineFormSetsView, EnhancedInlineFormSet

from core.models import Factura
from core.forms import (
    CreateComprobante, CreateItemFacturaForm, CreateTributoFacturaForm,
    CreateComprobanteAsociadoForm)


class IndexView(ListView):
    template_name = "frontend/index.html"

    def get_queryset(self):
        self.queryset = Factura.objects.all()
        return self.queryset


class CreateComprobanteView(InlineFormSetsView):
    model = Factura
    form_class = CreateComprobante
    template_name = "core/comprobante_form.html"

    class ItemFacturaInline(EnhancedInlineFormSet):
        form_class = CreateItemFacturaForm
        extra = 3
        can_delete = False

    class TributoFacturaInline(EnhancedInlineFormSet):
        form_class = CreateTributoFacturaForm
        extra = 3
        can_delete = False

    class ComprobanteAsociadoInline(EnhancedInlineFormSet):
        form_class = CreateComprobanteAsociadoForm
        extra = 3
        can_delete = False

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, "Comprobante creado exitosamente.")
        return reverse_lazy('index')

    formsets = [ItemFacturaInline, TributoFacturaInline, ComprobanteAsociadoInline,]


index = IndexView.as_view()
comprobante_nuevo = CreateComprobanteView.as_view()