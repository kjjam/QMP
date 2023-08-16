from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

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
