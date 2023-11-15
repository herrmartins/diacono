from django.views.generic import MonthArchiveView
from treasury.models import TransactionModel, MonthlyBalance
from dateutil.relativedelta import relativedelta
from datetime import date


class TransactionMonthArchiveView(MonthArchiveView):
    model = TransactionModel
    date_field = "date"  # The field that stores the date
    month_format = "%m"  # Format for the month
    allow_future = False
    template_name = "treasury/detailed_report.html"
    context_object_name = "finance_entries"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year"] = self.get_year()
        context["month"] = self.get_month()
        subtotal = []

        transactions = TransactionModel.objects.filter(
            date__month=context["month"], date__year=context["year"]
        ).order_by("date")

        previous_month = date(self.get_year(), self.get_month(), 1)

        previous_month += relativedelta(months=-1)
        try:
            balance_for_calc = MonthlyBalance.objects.get(month=previous_month).balance
        except MonthlyBalance.DoesNotExist:
            balance_for_calc = 0

        for fe in transactions:
            balance_for_calc += fe.amount
            subtotal.append(balance_for_calc)

        context["total"] = balance_for_calc
        context["subtotal"] = subtotal
        context["finance_entries"] = transactions
        context["counter"] = 0

        return context
