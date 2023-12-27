from django.views.generic import CreateView
from treasury.models import MonthlyBalance
from treasury.forms import InitialBalanceForm
from django.contrib.auth.mixins import PermissionRequiredMixin
import logging

logger = logging.getLogger(__name__)


class InitialBalanceCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'treasury.add_transactionmodel'
    model = MonthlyBalance
    form_class = InitialBalanceForm
    template_name = "treasury/monthly_balance_created.html"
    success_url = "/treasury/"
    
    def form_valid(self, form):
        logger.info("Form is valid")
        instance = form.save(commit=False)
        logger.debug(f"Instance data: {instance}")
        # Other logging statements or checks
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning("Form is invalid")
        logger.debug(f"Form errors: {form.errors}")
        print("ERRO:",form.errors)
        # Other logging statements or checks
        return super().form_invalid(form)
