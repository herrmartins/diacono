from django import forms
from secretarial.models import MinuteProjectModel
from datetime import date
from users.models import CustomUser, UsersFunctions


class MinuteProjectModelForm(forms.ModelForm):
    class Meta:
        model = MinuteProjectModel
        fields = "__all__"
        exclude = ["body"]

        labels = {
            "meeting_date": "Data da assembléia",
            "last_months_balance": "Saldo anterior",
            "previous_minute_reading": "Houve leitura da ata?",
            "previous_finance_report_reading": "Houve leitura do financeiro lido?",
            "number_of_attendees": "Número de presentes",
            "revenue": "Entradas",
            "expenses": "Saídas",
            "meeting_agenda": "Assuntos",
        }

        widgets = {
            "meeting_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "value": date.today(),
                }
            ),
            "number_of_attendees": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "previous_minute_reading": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "previous_finance_report_reading": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "last_months_balance": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "revenue": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "expenses": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "meeting_agenda": forms.SelectMultiple(
                attrs={
                    "class": "grid-item d-inline form-control my-2",
                }
            ),
        }

    president = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(
            functions__function__in=[UsersFunctions.Types.PASTOR, UsersFunctions.Types.MODERATOR]),
        widget=forms.Select(
            attrs={"class": "grid-item d-inline form-control my-2"}), label="Presidente",
    )
    secretary = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(
            functions__function=UsersFunctions.Types.SECRETARY),
        widget=forms.Select(
            attrs={"class": "grid-item d-inline form-control my-2"}), label="Secretário",
    )
    treasurer = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(
            functions__function=UsersFunctions.Types.TREASURER),
        widget=forms.Select(
            attrs={"class": "grid-item form-control my-2"}), label="Tesoureiro",
    )
    minute_reading_acceptance_proposal = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(type__in=[CustomUser.Types.STAFF, CustomUser.Types.REGULAR]).exclude(
            functions__function=UsersFunctions.Types.SECRETARY),
        widget=forms.Select(attrs={"class": "grid-item form-control my-2"}), label="Proposta de aceitação da ata",
    )

    minute_reading_acceptance_proposal_support = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(type__in=[CustomUser.Types.STAFF, CustomUser.Types.REGULAR]).exclude(
            functions__function=UsersFunctions.Types.SECRETARY),
        widget=forms.Select(attrs={"class": "grid-item form-control my-2"}), label="Apoio à proposta da ata",
    )

    finance_report_acceptance_proposal = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(type__in=[CustomUser.Types.STAFF, CustomUser.Types.REGULAR]).exclude(
            functions__function=UsersFunctions.Types.TREASURER),
        widget=forms.Select(attrs={"class": "grid-item d-inline form-control my-2"}), label="Proposta de aceitação do relatório financeiro",
    )

    finance_report_acceptance_proposal_support = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(type__in=[CustomUser.Types.STAFF, CustomUser.Types.REGULAR]).exclude(
            functions__function=UsersFunctions.Types.TREASURER),
        widget=forms.Select(attrs={"class": "grid-item form-control my-2"}), label="Apoio à proposta do relatório financeiro",
    )
