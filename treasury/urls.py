from django.urls import path
from treasury.views import (
    TreasuryHomeView,
    InitialBalanceCreateView,
    FinanceReportsListView,
    TransactionMonthArchiveView,
    TransactionDetailView,
    TransactionUpdateView,
    TransactionDeleteView,
)

app_name = "treasury"

urlpatterns = [
    path("", TreasuryHomeView.as_view(), name="home"),
    path(
        "balance/first",
        InitialBalanceCreateView.as_view(),
        name="create-initial-balance",
    ),
    path("reports", FinanceReportsListView.as_view(), name="list-financial-reports"),
    path(
        "reports/<int:year>/<int:month>/",
        TransactionMonthArchiveView.as_view(),
        name="monthly-transactions",
    ),
    path(
        "transaction/<int:pk>",
        TransactionDetailView.as_view(),
        name="transaction-detail",
    ),
    path("transaction/update/<int:pk>",
         TransactionUpdateView.as_view(), name="transaction-update"),
    path("transaction/delete/<int:pk>",
         TransactionDeleteView.as_view(), name="transaction-delete"),
]
