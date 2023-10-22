from django.contrib import admin
from treasury.models import (
    TransactionModel,
    TransactionEditHistory,
    CategoryModel,
    MonthlyBalance,
)

admin.site.register(TransactionModel)
admin.site.register(TransactionEditHistory)
admin.site.register(CategoryModel)
admin.site.register(MonthlyBalance)
