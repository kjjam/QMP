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
