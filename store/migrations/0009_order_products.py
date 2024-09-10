# Generated by Django 5.1 on 2024-09-05 13:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0008_alter_orderitem_quantity_alter_product_brand"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order_Products",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "orderitem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.orderitem",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="store.product",
                    ),
                ),
            ],
        ),
    ]
