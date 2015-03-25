__author__ = 'm4tuu'
from django import template


register = template.Library()


@register.inclusion_tag(
    'frontend/tags/form_as_row_table.html',
)
def render_formset_as_table(formset, title='Title'):
    return {
        'formset': formset,
        'title': title
    }
