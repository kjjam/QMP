# Generated by Django 4.2.4 on 2023-08-15 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash_managemnet', '0002_transaction_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(auto_created=True),
        ),
    ]
