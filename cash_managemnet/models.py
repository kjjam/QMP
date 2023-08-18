from django.db import models, transaction
from django.db.models import Sum
from rest_framework.authtoken.admin import User


class Category(models.Model):
    """
    info :
        Category model to store transaction assumption e.g groceries, apartment rent
    fields :
        name: name of category (max length = 50 characters)
    """
    name = models.CharField(max_length=50)


class Balance(models.Model):
    """
    info :
        Balance model to store balance of a user
    fields :
        user:
            An authenticated User
        amnt:
            The value of balance . It should get negative !
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amnt = models.IntegerField(default=0)

    def update_balance_amount(self):
        # Iterate into Transactions, calculate expenses and incomes, then subtract them

        # get incomes of user
        incomes = Transaction.incomes.filter(user=self.user).aggregate(val=Sum("amount"))["val"]
        # get expenses of user
        expenses = Transaction.expenses.filter(user=self.user).aggregate(val=Sum("amount"))["val"]
        # income or expenses should not be null . null->0
        self.amnt = incomes if incomes else 0 - expenses if expenses else 0
        self.save()


class TransactionIncomeManager(models.Manager):
    """
    info:
        A Transaction manager to get incomes transaction.
    usage:
        Transaction.incomes.all()
    """

    def get_queryset(self):
        return super().get_queryset().filter(type=Transaction.TypeChoices.INCOME)


class TransactionExpenseManager(models.Manager):
    """
        info:
            A Transaction manager to get expenses transaction.
        usage:
            Transaction.expenses.all()
    """

    def get_queryset(self):
        return super().get_queryset().filter(type=Transaction.TypeChoices.EXPENSE)


class Transaction(models.Model):
    """
    info :
        Transaction model to store transaction information
    fields :
        user: foreign key to owner user
        amount: the value of transaction
        type: it can be E(expense) or I(income)
        category : foreign key to Category model
        date : The date of transaction. it is created automatically while transaction is being saved.
            it can be modified by the serializer.
    """

    class TypeChoices(models.TextChoices):
        """
        choices for 'type' field
        """
        EXPENSE = ("E", "Expense")
        INCOME = ("I", "Income")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    type = models.CharField(max_length=1, choices=TypeChoices.choices)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)  # 2020-01-01T12:12:12

    objects = models.Manager()  # first and default manager
    incomes = TransactionIncomeManager()  # Transaction.incomes.all()
    expenses = TransactionExpenseManager()  # Transaction.expenses.all()

    # query params to filter database
    #  /transaction?type=I&date__lt=2022-12-12T15:15:15
    #        =>  Transaction.objects.filter(type__exact="I", date__lt="2022-12-12T15:15:15")
    filtering_lookups = [
        ('type__exact', 'type',),
        ('category__exact', 'category'),
        ('amount__lt', 'amount__lt'),
        ('amount__gt', 'amount__gt'),
        ('date__lt', 'date__lt'),
        ('date_gt', 'date__gt')
    ]

    def save(self, *args, **kwargs):
        """
        -Overriding save function to update balance of the user.
        -is called by:
            serializer.update(),
            serializer.partial_update(),
            serializers.save()
        -The transaction is atomic so that creating transaction and updating balance should
            happens just together
        """
        with transaction.atomic():
            transact = super(Transaction, self).save(*args, **kwargs)
            balance, _ = Balance.objects.get_or_create(user=self.user)  # create of get balance object
            balance.update_balance_amount()
            return transact

    def delete(self, *args):
        """
        -Overriding delete function to recalculate the balance
        -is called by:
            model.delete()
        -The transaction is atomic so that deleting transaction and updating balance should
            happens just together
                """
        with transaction.atomic():
            super(Transaction, self).delete(*args)
            balance = Balance.objects.get(user=self.user)
            balance.update_balance_amount()
