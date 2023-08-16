
from rest_framework import serializers
from cash_managemnet.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField()

    class Meta:
        model = Transaction
        fields = ["id", "amount", "type", "category", "date"]

    def create(self, validated_data):
        transaction = Transaction.objects.create(user=self.context["request"].user, **validated_data)
        return transaction
