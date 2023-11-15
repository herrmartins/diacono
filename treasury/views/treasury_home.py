from django.views.generic import TemplateView
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from treasury.forms import TransactionForm, InitialBalanceForm
from treasury.models import MonthlyBalance


class TreasuryHomeView(TemplateView):
    template_name = "treasury/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        balance_count = MonthlyBalance.objects.count()
        if balance_count > 0:
            current_date = timezone.now()
            previous_month = current_date - relativedelta(months=1)

            previous_month_balance = MonthlyBalance.objects.get(
                month__month=previous_month.month, month__year=previous_month.year)

            context[
                "previous_month_account_balance"
            ] = f"R$ {previous_month_balance.balance}"

            form = TransactionForm(user=self.request.user)
            context["form_transaction"] = form
        else:
            context["form_balance"] = InitialBalanceForm

        return context
