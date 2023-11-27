from django.views.generic import CreateView
from treasury.models import (
    TransactionModel,
    MonthlyBalance,
    MonthlyReportModel,
    MonthlyTransactionByCategoryModel,
)
from treasury.forms import GenerateFinanceReportModelForm
from django.http import HttpResponse
from datetime import datetime


class MonthlyReportCreateView(CreateView):
    model = MonthlyReportModel
    template_name = "treasury/create_monthly_report.html"
    success_url = "/treasury"
    form_class = GenerateFinanceReportModelForm
