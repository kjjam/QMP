from django.db import models
from django.db.models import Sum, Q
from rest_framework.authtoken.admin import User


class Category(models.Model):
    name = models.CharField(max_length=50)


class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amnt = models.IntegerField(default=0)

    def update_balance_amount(self):
        expense_income = Transaction.objects.filter(user=self.user).aggregate(
            expense=Sum("amount", filter=Q(type=Transaction.TypeChoices.EXPENSE)),
            income=Sum("amount", filter=Q(type=Transaction.TypeChoices.INCOME)),
        )
        self.amnt = expense_income["income"] - expense_income["expense"]
        self.save()


class Transaction(models.Model):
    class TypeChoices(models.TextChoices):
        EXPENSE = ("E", "Expense")
        INCOME = ("I", "Income")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
    type = models.CharField(max_length=1, choices=TypeChoices.choices)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    filtering_lookups = [
        ('type__exact', 'type',),
        ('category__exact', 'category'),
        ('amount__lt', 'amount__lt'),
        ('amount__gt', 'amount__gt'),
        ('date__lt', 'date__lt'),
        ('date_gt', 'date__gt')
    ]

    def save(self, *args, **kwargs):
        transaction = super(Transaction, self).save(*args, **kwargs)
        balance, _ = Balance.objects.get_or_create(user=self.user)
        balance.update_balance_amount()
        return transaction
