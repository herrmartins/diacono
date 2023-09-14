from django.contrib import admin
from .models import CustomUser, UsersFunctions

admin.site.register(CustomUser)
admin.site.register(UsersFunctions)
