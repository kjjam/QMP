from datetime import datetime

from django.db.models import Sum, Q, F
from django.db.models.functions import TruncMonth
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cash_managemnet.models import Transaction
from cash_managemnet.serializers import TransactionSerializer


class CreateTransactionView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    model = Transaction
    serializer_class = TransactionSerializer


class UpdateTransactionView(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class DeleteTransactionView(DestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    model = Transaction

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class GetTransactionView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    model = Transaction
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class GetAllTransactionView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    model = Transaction
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def filter_queryset(self, queryset):
        filter_lookups = {}
        for name, value in Transaction.filtering_lookups:
            param = self.request.GET.get(value)
            if param:
                filter_lookups[name] = param
        order_by = self.request.GET.get("order_by")
        if order_by is None or order_by not in [f.name for f in self.model._meta.get_fields()]:
            order_by = "id"
        return queryset.filter(**filter_lookups).order_by(order_by)


class GenerateReportMonthly(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        expected_args = ["date__lt", "date__gt"]
        filter_lookups = {}
        request_args = request.GET
        for arg in expected_args:
            if value := request_args.get(arg):
                filter_lookups[arg] = value
        transactions = Transaction.objects.filter(user=request.user, **filter_lookups).annotate(
            month=TruncMonth("date")).values("month").annotate(
            expenses=Sum("amount", filter=Q(type=Transaction.TypeChoices.EXPENSE)),
            incomes=Sum("amount", filter=Q(type=Transaction.TypeChoices.INCOME)),
        ).values("month", "expenses", "incomes")

        return Response(transactions, status=200)
