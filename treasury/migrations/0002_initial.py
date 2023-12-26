# Generated by Django 4.2.5 on 2023-12-26 19:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("treasury", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="transactionmodel",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="transactionedithistory",
            name="previous_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="previous_edits",
                to=settings.AUTH_USER_MODEL,
            ),
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
        migrations.AddField(
            model_name="monthlytransactionbycategorymodel",
            name="report",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="treasury.monthlyreportmodel",
            ),
        ),
    ]