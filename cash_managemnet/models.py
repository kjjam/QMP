from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)


class Transaction(models.Model):
    class TypeChoices(models.TextChoices):
        EXPENSE = ("E", "Expense")
        INCOME = ("I", "Income")

    amount = models.PositiveIntegerField(default=1)
    type = models.CharField(max_length=1, choices=TypeChoices.choices)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
