from django.views.generic import ListView
from treasury.models import MonthlyBalance


class FinanceReportsListView(ListView):
    template_name = "treasury/reports_list.html"
    model = MonthlyBalance
    context_object_name = "reports"
