# Generated by Django 4.2.4 on 2023-08-15 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash_managemnet', '0003_alter_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
