from django.views.generic import CreateView
from treasury.models import MonthlyBalance
from treasury.forms import InitialBalanceForm


class InitialBalanceCreateView(CreateView):
    model = MonthlyBalance
    form_class = InitialBalanceForm
    template_name = "treasury/monthly_balance_created.html"
    success_url = "/treasury/"
