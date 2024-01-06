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
        ]
        widgets = {
            "user": forms.HiddenInput(),
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
        custom_user = cleaned_data.get("custom_user")

        if not contact_name and not custom_user:
            self.add_error("contact_name", "Please provide contact information.")
            raise forms.ValidationError("Please provide contact information.")

        if contact_name and custom_user:
            # Instead of raising an error, prioritize custom_user as contact
            cleaned_data["contact_info"] = custom_user

        return cleaned_data