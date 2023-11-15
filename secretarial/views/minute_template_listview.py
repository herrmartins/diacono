from django.views.generic import ListView
from secretarial.models import MinuteTemplateModel


class MinuteTemplatesListView(ListView):
    model = MinuteTemplateModel
    template_name = 'secretarial/list_templates.html'
    context_object_name = 'templates'
