from django import forms
from django.core.exceptions import ValidationError
from users.models import CustomUser


class UpdateUserRoleModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("functions", "type")
        labels = {
            "functions": "Funções",
            "type": "Status"
        }
        widgets = {
            "functions": forms.SelectMultiple(
                attrs={
                    "class": "grid-item d-inline form-control my-2",
                }
            ),
            "type": forms.Select(
                attrs={
                    "class": "grid-item d-inline form-control my-2",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('type')
        functions = cleaned_data.get('functions')

        if user_type in (
            CustomUser.Types.CONGREGATED, CustomUser.Types.SIMPLE_USER
        ) and functions:
            raise ValidationError(
                "Congregados e usuários simples não podem ter função.")
