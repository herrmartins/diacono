from django import forms
from treasury.models import (
    MonthlyBalance,
    MonthlyReportModel,
    MonthlyTransactionByCategoryModel,
)


class GenerateFinanceReportModelForm(forms.ModelForm):

    class Meta:
        model = MonthlyReportModel
        fields = "__all__"
        exclude = ("ativo",)

        labels = {
            "month": "Mês:",
            "previous_month_balance": "Saldo do mês anterior:",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["month"].widget = forms.HiddenInput()
        self.fields["previous_month_balance"].widget = forms.NumberInput(
            attrs={"class": "form-control bg-light", "readonly": True}
        )
        self.fields["total_positive_transactions"].widget = forms.NumberInput(
            attrs={"class": "form-control bg-light", "readonly": True}
        )
        self.fields["total_negative_transactions"].widget = forms.NumberInput(
            attrs={"class": "form-control bg-light", "readonly": True}
        )
        self.fields["in_cash"].widget = forms.NumberInput(
            attrs={"class": "form-control"}
        )
        self.fields["in_current_account"].widget = forms.NumberInput(
            attrs={"class": "form-control"}
        )
        self.fields["in_savings_account"].widget = forms.NumberInput(
            attrs={"class": "form-control"}
        )
        self.fields["total_balance"].widget = forms.NumberInput(
            attrs={"class": "form-control bg-light", "readonly": True}
        )

        initial_date = self.initial.get('month')
        if initial_date:
            self.initial['month'] = initial_date.strftime('%Y-%m-%d')
