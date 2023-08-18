from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cash_managemnet.models import Transaction
from cash_managemnet.serializers import TransactionSerializer


class CreateTransactionView(CreateAPIView):
    """
    url : /insert-transaction
    info : Genetic View to create new Transaction
        creation is mainly done by the SignupSerializer
    headers =
        Content-Type : application/json
        Authorization : Token <token>
    method: POST
    request body:
        {"amount": 200, "type": "E", category": 1, "date": "2023-08-18T16:32:59.594691Z"}
    response body:
        {"id":1, "amount": 200, "type": "E", category": 1, "date": "2023-08-18T16:32:59.594691Z"}
    """

    permission_classes = [IsAuthenticated, ]
    model = Transaction
    serializer_class = TransactionSerializer


class UpdateTransactionView(UpdateAPIView):
    """
    url : /update-transaction/<int:pk>
    info : Genetic View to update  Transaction
    headers =
        Content-Type : application/json
        Authorization : Token <token>
    method: PATCH(partial update), PUT(update)
    request body:
        {"amount": 200, "type": "E", category": 1, "date": "2023-08-18T16:32:59.594691Z"}
    response body:
        {"id":1, "amount": 200, "type": "E", category": 1, "date": "2023-08-18T16:32:59.594691Z"}
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        # User should update just his own transactions not the other's.
        return Transaction.objects.filter(user=self.request.user)


class DeleteTransactionView(DestroyAPIView):
    """
    url : /delete-transaction/<int:pk>
    info : Genetic View to delete a Transaction
    headers =
        Content-Type : application/json
        Authorization : Token <token>
    method: DELETE
    response status code = 204
    """
    permission_classes = [IsAuthenticated, ]
    model = Transaction

    def get_queryset(self):
        # User should delete just his own transactions not the other's.
        return Transaction.objects.filter(user=self.request.user)


class GetTransactionView(RetrieveAPIView):
    """
    url : /transaction/<int:pk>
    info : Genetic View to get Transaction with id provided
    headers =
        Content-Type : application/json
        Authorization : Token <token>
    method: GET
    response body:
        {"id":1, "amount": 200, "type": "E", category": 1, "date": "2023-08-18T16:32:59.594691Z"}
    """
    permission_classes = [IsAuthenticated, ]
    model = Transaction
    serializer_class = TransactionSerializer

    def get_queryset(self):
        # User should not access other's transactions.
        return Transaction.objects.filter(user=self.request.user)


class GetAllTransactionView(ListAPIView):
    """
    url : /transaction
    info : Get user all transactions with query params lookups(if needed)
            transaction?type=I   =>    Transaction.objects.filter(type__exact="I")
            transaction?amount__lt=200   =>    Transaction.objects.filter(amount__lt=200)
            transaction?amount__gt=100   =>    Transaction.objects.filter(amount__gt=100)
            transaction?date__lt=2020-02-20T20:20:20   =>    Transaction.objects.filter(date__lt=2020-02-20T20:20:20)
            transaction?date__gt=2020-02-20T20:20:20   =>    Transaction.objects.filter(date__gt=2019-01-19T19:19:19)
        ****transaction?q1=val1&q2=val2...     =>   Transaction.objects.filter(q'1=val1 , q'2=val2, ...)
    headers =
        Content-Type : application/json
        Authorization : Token <token>
    method: GET
    response body:
    [
        {"id":1, "amount": 200, "type": "E", category": 1, "date": "2023-08-18T16:32:59.594691Z"},
        {"id":20, "amount": 100, "type": "I", category": 2, "date": "2009-08-18T20:10:59.594691Z"}
        ...
    ]
    """
    permission_classes = [IsAuthenticated, ]
    model = Transaction
    serializer_class = TransactionSerializer

    def get_queryset(self):
        # User should not access other's transactions.
        return Transaction.objects.filter(user=self.request.user)

    def filter_queryset(self, queryset):
        # the function to apply query params in the result

        filter_lookups = {}
        # extract params from the url
        for name, value in Transaction.filtering_lookups:  # filtering_lookup in .models/Transaction model
            param = self.request.GET.get(value)
            if param:
                filter_lookups[name] = param

        order_by = self.request.GET.get("order_by")
        # check if order_by value is a valid field name (default = id)
        if order_by is None or order_by not in [f.name for f in self.model._meta.get_fields()]:
            order_by = "id"
        # apply all lookups found in url
        return queryset.filter(**filter_lookups).order_by(order_by)


class GenerateReportMonthly(APIView):
    """
    url : /report
    info : Generates monthly reports of expenses and incomes of the user
    headers =
        Content-Type : application/json
        Authorization : Token <token>
    method: GET
    response body:
        [
            {"month": "2023-08-01T00:00:00Z","expenses": 100,"incomes": 500}
            {"month": "2023-09-01T00:00:00Z","expenses": 150,"incomes": 400}
            {"month": "2023-010-01T00:00:00Z","expenses": 200,"incomes": null}
        ]
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        """
        Getting reports with filters
            /report?date__lt=2020-02-20T20:20:20  =>    e.g. Transaction.incomes.filter(date_lt=2020-02-20T20:20:20)
            /report?date__gt=2018-08-18T18:18:18 =>    e.g. Transaction.incomes.filter(date_gt=2018-08-18T18:18:18)
        *** /report?date__gt=...&date_lt=...
        """
        expected_args = ["date__lt", "date__gt"]
        filter_lookups = {}
        request_args = request.GET
        # extract params from the url
        for arg in expected_args:
            if value := request_args.get(arg):
                filter_lookups[arg] = value
        # get income and expense transactions
        transactions = Transaction.objects.filter(user=request.user, **filter_lookups).annotate(
            month=TruncMonth("date")).values("month").annotate(
            expenses=Sum("amount", filter=Q(type=Transaction.TypeChoices.EXPENSE)),
            incomes=Sum("amount", filter=Q(type=Transaction.TypeChoices.INCOME)),
        ).values("month", "expenses", "incomes")

        return Response(transactions, status=200)
