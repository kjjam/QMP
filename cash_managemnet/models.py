from django.db import models, transaction
from django.db.models import Sum, Q
from rest_framework.authtoken.admin import User


class Category(models.Model):
    name = models.CharField(max_length=50)


class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amnt = models.IntegerField(default=0)

    def update_balance_amount(self):
        incomes = Transaction.incomes.filter(user=self.user).aggregate(val=Sum("amount"))["val"]
        expenses = Transaction.expenses.filter(user=self.user).aggregate(val=Sum("amount"))["val"]

        self.amnt = incomes - expenses
        self.save()


class TransactionIncomeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=Transaction.TypeChoices.INCOME)


class TransactionExpenseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=Transaction.TypeChoices.EXPENSE)


class Transaction(models.Model):
    class TypeChoices(models.TextChoices):
        EXPENSE = ("E", "Expense")
        INCOME = ("I", "Income")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
    type = models.CharField(max_length=1, choices=TypeChoices.choices)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    incomes = TransactionIncomeManager()
    expenses = TransactionExpenseManager()

    filtering_lookups = [
        ('type__exact', 'type',),
        ('category__exact', 'category'),
        ('amount__lt', 'amount__lt'),
        ('amount__gt', 'amount__gt'),
        ('date__lt', 'date__lt'),
        ('date_gt', 'date__gt')
    ]

    def save(self, *args, **kwargs):
        with transaction.atomic():
            transact = super(Transaction, self).save(*args, **kwargs)
            balance, _ = Balance.objects.get_or_create(user=self.user)
            balance.update_balance_amount()
            return transact

    def delete(self, *args):
        with transaction.atomic():
            super(Transaction, self).delete(*args)
            balance, _ = Balance.objects.get(user=self.user)
            balance.update_balance_amount()
