from django import forms
from events.models import Event
from users.models import CustomUser


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "start_date",
            "end_date",
            "price",
            "location",
            "contact_user",
            "contact_name",
            "category",
        ]
        widgets = {
            "user": forms.HiddenInput(),
            "start_date": forms.DateTimeInput(
                attrs={"class": "form-control", 'type': 'datetime-local'}),
            "end_date": forms.DateTimeInput(
                attrs={"class": "form-control", 'type': 'datetime-local'}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "contact_name": forms.TextInput(attrs={"class": "form-control"}),
            "contact_user": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}),
            "location": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(EventForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields["user"] = forms.ModelChoiceField(
                queryset=CustomUser.objects.filter(pk=user.pk),
                empty_label=None,
                initial=user,
            )
            self.fields["user"].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        contact_name = cleaned_data.get("contact_name")
        custom_user = cleaned_data.get("contact_user")

        if not contact_name and not custom_user:
            self.add_error(
                "contact_name", "Please provide contact information.")
            raise forms.ValidationError("Please provide contact information.")

        if contact_name and custom_user:
            # Instead of raising an error, prioritize custom_user as contact
            cleaned_data["contact_user"] = custom_user
            cleaned_data["contact_name"] = ""

        return cleaned_data
