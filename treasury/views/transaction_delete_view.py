from django.views.generic.edit import DeleteView
from treasury.models import TransactionModel
from django.shortcuts import reverse


class TransactionDeleteView(DeleteView):
    template_name = "treasury/transaction_deleted.html"
    model = TransactionModel
    context_object_name = "transaction"

    def get_success_url(self):
        return reverse(
            "treasury:monthly-transactions",
            kwargs={"month": self.object.date.month, "year": self.object.date.year},
        )
