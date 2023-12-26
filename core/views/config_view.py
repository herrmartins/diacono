from django.views.generic import TemplateView


class ConfigView(TemplateView):
    template_name = 'core/config.html'
