from django.views.generic import TemplateView
# from secretarial.forms import SearchMinuteForm


class SecretarialHomeView(TemplateView):
    template_name = 'secretarial/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["search_form"] = SearchMinuteForm

        return context
