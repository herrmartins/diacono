from django.contrib import admin
from .models import CustomUser, UsersFunctions
from django.core.exceptions import ValidationError


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'type')

    def save_model(self, request, obj, form, change):
        if obj.type in (CustomUser.Types.CONGREGATED, CustomUser.Types.SIMPLE_USER):
            initial_functions = form.initial.get('functions', [])
            current_functions = form.cleaned_data.get('functions', [])

            if len(initial_functions) != len(current_functions):
                raise ValidationError(
                    "Congregated and Simple Users cannot have modified functions."
                )

        super().save_model(request, obj, form, change)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UsersFunctions)
