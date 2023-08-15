from rest_framework.serializers import ModelSerializer

from cash_managemnet.models import Transaction


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "amount", "type", "category", "date"]

    def create(self, validated_data):
        transaction = Transaction.objects.create(user=self.context["request"].user, **validated_data)
        return transaction
