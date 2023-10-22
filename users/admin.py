from django.contrib import admin
from .models import CustomUser, UsersFunctions
from django.core.exceptions import ValidationError


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'type')

    def save_model(self, request, obj, form, change):
        # Check if the user type is CONGREGATED or SIMPLE_USER
        if obj.type in (CustomUser.Types.CONGREGATED, CustomUser.Types.SIMPLE_USER):
            # Check if functions are being added or removed
            if form.cleaned_data['functions'].count() != form.initial['functions'].count():
                raise ValidationError(
                    "Congregados e meros usuários não podem ter funções.")
        super().save_model(request, obj, form, change)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UsersFunctions)
