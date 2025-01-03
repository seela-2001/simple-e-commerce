# Generated by Django 5.1 on 2024-08-20 17:04

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                ("payment_method", models.CharField(default="visa", max_length=100)),
                ("is_paid", models.BooleanField(default=False)),
                ("is_delivered", models.BooleanField(default=False)),
                ("paid_at", models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Review",
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
                ("text", models.TextField(blank=True, max_length=300, null=True)),
                (
                    "rating",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_reviews",
                        to="store.product",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_review",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
