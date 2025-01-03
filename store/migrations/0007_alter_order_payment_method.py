# Generated by Django 5.1 on 2024-09-02 11:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0006_alter_order_payment_method"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="payment_method",
            field=models.CharField(
                choices=[("visa", "visa"), ("cash", "cash"), ("fawry", "fawry")],
                default="visa",
                max_length=100,
            ),
        ),
    ]
