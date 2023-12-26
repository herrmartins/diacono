from django.views.generic import TemplateView
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.shortcuts import get_object_or_404
from treasury.forms import TransactionForm, InitialBalanceForm
from treasury.models import MonthlyBalance
from django.contrib.auth.mixins import PermissionRequiredMixin


class TreasuryHomeView(PermissionRequiredMixin, TemplateView):
    permission_required = 'treasury.view_transactionmodel'
    template_name = "treasury/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        balance_count = MonthlyBalance.objects.count()
        current_date = timezone.now()
        if balance_count > 0:
            previous_month = current_date - relativedelta(months=1)
            previous_month_balance = get_object_or_404(
                MonthlyBalance,
                month__month=previous_month.month,
                month__year=previous_month.year,
            )

            context[
                "previous_month_account_balance"
            ] = f"R$ {previous_month_balance.balance}"

            form = TransactionForm(user=self.request.user)
            context["form_transaction"] = form
            context["month"] = current_date.month
            context["year"] = current_date.year
        else:
            context["form_balance"] = InitialBalanceForm

        return context
