from rest_framework import serializers

from cash_managemnet.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(required=False)

    class Meta:
        model = Transaction
        fields = ["id", "amount", "type", "category", "date"]


    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        transaction = super(TransactionSerializer, self).create(validated_data)
        return transaction
