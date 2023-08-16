from django.urls import path

from cash_managemnet.views import CreateTransactionView, UpdateTransactionView, DeleteTransactionView, \
    GetTransactionView, GetAllTransactionView, GenerateReportMonthly

urlpatterns = [
    path("insert-transaction", CreateTransactionView.as_view()),
    path("update-transaction/<int:pk>", UpdateTransactionView.as_view()),
    path("delete-transaction/<int:pk>", DeleteTransactionView.as_view()),
    path("transaction/<int:pk>", GetTransactionView.as_view()),
    path("transaction/", GetAllTransactionView.as_view()),
    path("report", GenerateReportMonthly.as_view())

]
