from rest_framework import serializers

from cash_managemnet.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
    info: serializer for registering the Transaction,
    model: models.Transaction
    selected_fields = id, amount, type, category, date
    """

    # because the date field in the model is auto-add-now and not editable,
    #    so there should be another date field in this serializer
    date = serializers.DateTimeField(required=False)

    class Meta:
        model = Transaction
        fields = ["id", "amount", "type", "category", "date"]  # model fields

    def create(self, validated_data):
        """
        overriding create method to save current user as Transaction owner
        """
        validated_data["user"] = self.context["request"].user
        transaction = super(TransactionSerializer, self).create(validated_data)
        return transaction
