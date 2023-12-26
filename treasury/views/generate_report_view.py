from django.views.generic import TemplateView
from treasury.models import (
    TransactionModel,
    MonthlyBalance,
)
from treasury.forms import GenerateFinanceReportModelForm
from dateutil.relativedelta import relativedelta
from datetime import date
from django.http import HttpResponse, Http404
from datetime import datetime
from treasury.utils import (
    get_aggregate_transactions_by_category,
    get_total_transactions_amount,
)
from django.contrib.auth.mixins import PermissionRequiredMixin


class GenerateMonthlyReportView(PermissionRequiredMixin, TemplateView):
    permission_required = "add_monthlyreportmodel"
    template_name = "treasury/monthly_report_generator.html"

    def get(self, request, month, year, *args, **kwargs):
        current_date = datetime.now()
        current_month = current_date.month
        current_year = current_date.year

        if int(month) == current_month and int(year) == current_year:
            raise Http404("Não se pode criar relatório analítico do mês em curso...")

        try:
            month_year = datetime(int(year), int(month), 1)
            monthly_balance = MonthlyBalance.objects.get(month=month_year)
        except MonthlyBalance.DoesNotExist:
            raise Http404("Não há registros para esta data...")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        previous_month_balance = 0

        report_month = date(year, month, 1)

        previous_month = date(year, month, 1)

        previous_month += relativedelta(months=-1)

        last_day_of_previous_month = report_month
        last_day_of_previous_month += relativedelta(days=-1)

        try:
            balance_for_calc = MonthlyBalance.objects.get(month=previous_month).balance
            previous_month_balance = balance_for_calc
        except MonthlyBalance.DoesNotExist:
            balance_for_calc = 0

        transactions = TransactionModel.objects.filter(
            date__month=month, date__year=year
        ).order_by("date")

        for fe in transactions:
            balance_for_calc += fe.amount

        positive_transactions_dict = get_aggregate_transactions_by_category(
            year, month, True
        )
        negative_transactions_dict = get_aggregate_transactions_by_category(
            year, month, False
        )

        context["p_transactions"] = positive_transactions_dict
        context["total_ptransactions"] = get_total_transactions_amount(
            positive_transactions_dict
        )
        context["n_transactions"] = negative_transactions_dict
        context["total_ntransactions"] = get_total_transactions_amount(
            negative_transactions_dict
        )
        context["pm_balance"] = previous_month_balance

        initial_data = {
            "month": report_month,
            "previous_month_balance": previous_month_balance,
            "total_positive_transactions": context["total_ptransactions"],
            "total_negative_transactions": context["total_ntransactions"],
            "total_balance": balance_for_calc,
        }

        context["form"] = GenerateFinanceReportModelForm(initial=initial_data)
        return context
