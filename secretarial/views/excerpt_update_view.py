from django.views.generic import UpdateView
from secretarial.models import MinuteExcerptsModel


class ExcerptUpdateView(UpdateView):
    model = MinuteExcerptsModel
    template_name = 'secretarial/excerpt_updated.html'
    fields = ['title', 'excerpt']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instance'] = self.object
        return context
