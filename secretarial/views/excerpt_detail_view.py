from django.views.generic import DetailView
from secretarial.models import MinuteExcerptsModel


class ExcerptDetailView(DetailView):
    model = MinuteExcerptsModel
    template_name = 'secretarial/excerpt_detail.html'
    context_object_name = 'excerpt'
