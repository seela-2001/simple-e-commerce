# Generated by Django 5.1 on 2024-09-06 12:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0009_order_products"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="tax_price",
            field=models.FloatField(default=0),
        ),
    ]
