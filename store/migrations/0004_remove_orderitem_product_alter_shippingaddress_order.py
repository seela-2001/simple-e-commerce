# Generated by Django 5.1 on 2024-08-25 15:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0003_order_delivered_at_order_price_order_shipping_price_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderitem",
            name="product",
        ),
        migrations.AlterField(
            model_name="shippingaddress",
            name="order",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_shipping",
                to="store.order",
            ),
        ),
    ]