from django import forms
from django.forms import ModelForm
from users.models import CustomUser
from django.forms.widgets import DateInput
from bootstrap_datepicker_plus.widgets import DatePickerInput


class UpdateUserProfileModelForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "address",
            "phone_number",
            "is_whatsapp",
            "date_of_birth",
            "about",
        )

        labels = {
            "first_name": "",
            "last_name": "",
            "email": "",
            "address": "",
            "phone_number": "",
            "is_whatsapp": "Whatsapp?",
            "date_of_birth": "",
            "about": "",
        }

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control my-2",
                    "placeholder": "Prenome",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control my-2",
                    "placeholder": "Sobrenome",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control my-2",
                    "placeholder": "E-mail",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control my-2",
                    "placeholder": "Endereço",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control my-2",
                    "placeholder": "Phone",
                }
            ),
            "date_of_birth": DatePickerInput(
                format=("%d-%m-%Y"),
                attrs={
                    "class": "datepicker form-control my-2",
                    "placeholder": "Data",
                },
            ),
            "about": forms.Textarea(
                attrs={
                    "class": "form-control my-2",
                    "placeholder": "Sobre você...",
                }
            ),
        }
