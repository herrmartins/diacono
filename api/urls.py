from django.urls import path
from . import views

urlpatterns = [
    path("", views.getData),
    path("users", views.SearchUsersListCreateAPIView.as_view(), name="search-users"),
    path(
        "members", views.SearchMembersListCreateAPIView.as_view(), name="search-members"
    ),
    path(
        "templates",
        views.SearchTemplatesListCreateAPIView.as_view(),
        name="search-templates",
    ),
    path(
        "minutes", views.SearchMinutesListCreateAPIView.as_view(), name="search-minutes"
    ),
    path(
        "transactions",
        views.TransactionCatListAPIView.as_view(),
        name="get-transactions",
    ),
    path(
        "transactions/post",
        views.TransactionsCreateAPIView.as_view(),
        name="post-transaction",
    ),
    path("getbalance", views.getCurrentBalance, name="get-current-balance"),
    path(
        "api/transaction/<int:pk>/delete",
        views.DeleteTransaction.as_view(),
        name="delete-transaction",
    ),
    path("search", views.unifiedSearch, name="secretarial-search"),
]
