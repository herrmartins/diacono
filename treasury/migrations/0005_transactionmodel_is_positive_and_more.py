# Generated by Django 4.2.5 on 2023-10-23 11:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("treasury", "0004_alter_monthlybalance_is_first_month_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="transactionmodel",
            name="is_positive",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="transactionmodel",
            name="edit_history",
            field=models.ManyToManyField(
                blank=True, to="treasury.transactionedithistory"
            ),
        ),
    ]