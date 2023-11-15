# Generated by Django 4.2.5 on 2023-10-21 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CategoryModel",
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
                    "created",
                    models.DateField(auto_now_add=True, verbose_name="Data de Criação"),
                ),
                (
                    "modified",
                    models.DateField(
                        auto_now_add=True, verbose_name="Data de Atualização"
                    ),
                ),
                ("ativo", models.BooleanField(default=True, verbose_name="Ativo?")),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TransactionEditHistory",
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
                    "created",
                    models.DateField(auto_now_add=True, verbose_name="Data de Criação"),
                ),
                (
                    "modified",
                    models.DateField(
                        auto_now_add=True, verbose_name="Data de Atualização"
                    ),
                ),
                ("ativo", models.BooleanField(default=True, verbose_name="Ativo?")),
                ("original_description", models.CharField(max_length=255)),
                (
                    "original_amount",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("original_date", models.DateField()),
                ("edited_description", models.CharField(max_length=255)),
                ("edited_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "edited_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TransactionModel",
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
                    "created",
                    models.DateField(auto_now_add=True, verbose_name="Data de Criação"),
                ),
                (
                    "modified",
                    models.DateField(
                        auto_now_add=True, verbose_name="Data de Atualização"
                    ),
                ),
                ("ativo", models.BooleanField(default=True, verbose_name="Ativo?")),
                ("description", models.CharField(max_length=255)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("date", models.DateField()),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="treasury.categorymodel",
                    ),
                ),
                (
                    "edit_history",
                    models.ManyToManyField(to="treasury.transactionedithistory"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Transação",
                "verbose_name_plural": "Transações",
            },
        ),
        migrations.AddField(
            model_name="transactionedithistory",
            name="transaction",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="treasury.transactionmodel",
            ),
        ),
        migrations.AddField(
            model_name="transactionedithistory",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="MonthlyBalance",
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
                    "created",
                    models.DateField(auto_now_add=True, verbose_name="Data de Criação"),
                ),
                (
                    "modified",
                    models.DateField(
                        auto_now_add=True, verbose_name="Data de Atualização"
                    ),
                ),
                ("ativo", models.BooleanField(default=True, verbose_name="Ativo?")),
                ("month", models.DateField()),
                (
                    "initial_balance",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "balance",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
