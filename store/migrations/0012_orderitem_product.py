# Generated by Django 5.1 on 2024-09-09 17:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0011_order_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="product",
            field=models.ManyToManyField(
                through="store.Order_Products", to="store.product"
            ),
        ),
    ]
