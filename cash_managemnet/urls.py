from django.urls import path

from cash_managemnet.views import CreateTransactionView, UpdateTransactionView, DeleteTransactionView

urlpatterns = [
    path("insert-transaction", CreateTransactionView.as_view()),
    path("update-transaction/<int:pk>", UpdateTransactionView.as_view()),
    path("delete-transaction/<int:pk>", DeleteTransactionView.as_view())
]
