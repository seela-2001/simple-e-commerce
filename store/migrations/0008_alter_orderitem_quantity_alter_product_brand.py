# Generated by Django 5.1 on 2024-09-05 13:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0007_alter_order_payment_method"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="quantity",
            field=models.IntegerField(
                default=0, validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="brand",
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                validators=[django.core.validators.MinLengthValidator(3)],
            ),
        ),
    ]
