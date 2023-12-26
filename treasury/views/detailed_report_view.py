from django.views.generic import MonthArchiveView
from treasury.models import TransactionModel, MonthlyBalance
from dateutil.relativedelta import relativedelta
from datetime import date
from django.contrib.auth.mixins import PermissionRequiredMixin


class TransactionMonthArchiveView(PermissionRequiredMixin, MonthArchiveView):
    permission_required = 'treasury.view_transactionmodel'
    model = TransactionModel
    date_field = "date"
    month_format = "%m"
    allow_future = False
    template_name = "treasury/detailed_report.html"
    context_object_name = "finance_entries"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year"] = self.get_year()
        context["month"] = self.get_month()
        subtotal = []
        previous_month_balance = 0
        current_date = date.today()
        not_current_date = True

        if (
            current_date.month == context["month"]
            and current_date.year == context["year"]
        ):
            not_current_date = False

        transactions = TransactionModel.objects.filter(
            date__month=context["month"], date__year=context["year"]
        ).order_by("date")

        previous_month = date(self.get_year(), self.get_month(), 1)

        previous_month += relativedelta(months=-1)
        try:
            balance_for_calc = MonthlyBalance.objects.get(month=previous_month).balance
            previous_month_balance = balance_for_calc
        except MonthlyBalance.DoesNotExist:
            balance_for_calc = 0

        for fe in transactions:
            balance_for_calc += fe.amount
            subtotal.append(balance_for_calc)

        context["total"] = balance_for_calc
        context["subtotal"] = subtotal
        context["finance_entries"] = transactions
        context["counter"] = 0
        context["balance"] = previous_month_balance
        context["ncd"] = not_current_date

        return context
