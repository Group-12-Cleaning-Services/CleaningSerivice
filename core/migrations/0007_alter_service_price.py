# Generated by Django 4.2.9 on 2024-01-11 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_balance_transaction_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=100),
        ),
    ]