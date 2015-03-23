from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView

from core.models import Factura
from core.forms import CreateComprobante


class Index(ListView):
    template_name = "frontend/index.html"

    def get_queryset(self):
        self.queryset = Factura.objects.all()
        return self.queryset


class CreateComprobante(CreateView):
    model = Factura
    form_class = CreateComprobante
    template_name = "core/comprobante_form.html"

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, "Comprobante creado exitosamente.")
        return reverse_lazy('index')


index = Index.as_view()
comprobante_nuevo = CreateComprobante.as_view()