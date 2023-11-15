from django.views.generic.edit import DeleteView
from secretarial.models import MinuteExcerptsModel
from django.urls import reverse


class ExcerptDeleteView(DeleteView):
    model = MinuteExcerptsModel
    template_name = "secretarial/excerpt_deleted.html"

    def get_success_url(self):
        return reverse('secretarial:list-excerpts')
