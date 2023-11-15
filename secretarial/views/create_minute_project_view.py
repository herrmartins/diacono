from django.views.generic import CreateView
from secretarial.forms import MinuteProjectModelForm
from django.urls import reverse_lazy


class CreateMinuteProjectView(CreateView):
    model = MinuteProjectModelForm
    form_class = MinuteProjectModelForm
    template_name = "secretarial/minute_home.html"
    success_url = reverse_lazy("secretarial:minute-home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = MinuteProjectModelForm
        return context
