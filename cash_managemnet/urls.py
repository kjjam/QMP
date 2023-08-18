from django.urls import path

from cash_managemnet.views import CreateTransactionView, UpdateTransactionView, DeleteTransactionView, \
    GetTransactionView, GetAllTransactionView, GenerateReportMonthly

urlpatterns = [
    path("insert-transaction", CreateTransactionView.as_view(), name="insert-transaction"),
    path("update-transaction/<int:pk>", UpdateTransactionView.as_view(), name="update-transaction"),
    path("delete-transaction/<int:pk>", DeleteTransactionView.as_view(), name="delete-transaction"),
    path("transaction/<int:pk>", GetTransactionView.as_view(), name="transaction"),
    path("transaction/", GetAllTransactionView.as_view(), name="all-transaction"),
    path("report", GenerateReportMonthly.as_view(), name='report')

]
