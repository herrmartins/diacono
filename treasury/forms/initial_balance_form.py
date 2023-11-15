from django import forms
from treasury.models import MonthlyBalance


class InitialBalanceForm(forms.ModelForm):
    class Meta:
        model = MonthlyBalance
        fields = ["balance", "month"]

    balance = forms.DecimalField(
        label="Saldo Inicial",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    month = forms.DateField(
        label="Selecione o mês e ano",
        widget=forms.DateInput(attrs={"type": "month", "class": "form-control"}),
        input_formats=["%Y-%m"],
    )
