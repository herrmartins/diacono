from django.urls import reverse
from django.views.generic import UpdateView
from treasury.models import TransactionModel
from treasury.forms import TransactionForm


class TransactionUpdateView(UpdateView):
    model = TransactionModel
    form_class = TransactionForm
    template_name = "treasury/transaction_updated.html"
    context_object_name = "transaction"

    def get_success_url(self):
        return reverse('treasury:transaction-detail', kwargs={'pk': self.object.pk})
