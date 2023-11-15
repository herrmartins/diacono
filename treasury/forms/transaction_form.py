from django import forms
from treasury.models import TransactionModel
from django.forms.widgets import HiddenInput


class TransactionForm(forms.ModelForm):
    class Meta:
        model = TransactionModel
        fields = ['user', 'category', 'description', 'amount', 'date']
        labels = {
            'category': 'Categoria',
            'description': 'Descrição',
            'amount': 'Valor',
            'date': 'Data'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['user'].initial = user
        self.fields['user'].widget = HiddenInput()

        self.fields['category'].widget.attrs['class'] = 'form-select'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['amount'].widget.attrs['class'] = 'form-control'
        self.fields['date'].widget = forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'})

        initial_date = self.initial.get('date')
        if initial_date:
            self.initial['date'] = initial_date.strftime('%Y-%m-%d')
