from django.template import Library
from ..models import Tag

register=Library()

@register.inclusion_tag('includes/sidebar.html')
def sidebar_view(tag=None):
    categories=Tag.objects.all()
    context={
        'categories':categories,
        'tag':tag
    }
    return context