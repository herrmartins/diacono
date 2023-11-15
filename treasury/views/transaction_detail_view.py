from django.views.generic import DetailView
from treasury.models import TransactionModel
from treasury.forms import TransactionForm


class TransactionDetailView(DetailView):
    model = TransactionModel
    template_name = "treasury/transaction_detail.html"
    context_object_name = "transaction"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the object being viewed
        transaction = self.get_object()

        initial_data = {
            "user": self.request.user,
            "category": transaction.category,
            "description": transaction.description,
            "amount": transaction.amount,
            "date": transaction.date,
        }
        form = TransactionForm(initial=initial_data)

        # Add the form to the context
        context["form"] = form

        return context
