# Generated by Django 4.2.5 on 2023-10-13 23:03

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("secretarial", "0004_minuteexcerptsmodel"),
    ]

    operations = [
        migrations.CreateModel(
            name="MinuteProjectModel",
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
                ("meeting_date", models.DateField()),
                ("number_of_atendees", models.CharField(max_length=3)),
                ("previous_minute_reading", models.BooleanField(default=True)),
                ("previous_finance_report_reading", models.BooleanField(default=True)),
                (
                    "last_months_balance",
                    models.DecimalField(decimal_places=2, max_digits=8),
                ),
                ("revenue", models.DecimalField(decimal_places=2, max_digits=8)),
                ("expenses", models.DecimalField(decimal_places=2, max_digits=8)),
                ("body", ckeditor.fields.RichTextField(blank=True, null=True)),
                (
                    "finance_report_acceptance_proposal",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="fr_acceptor",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "finance_report_acceptance_proposal_support",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="fr_supporter",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "meeting_agenda",
                    models.ManyToManyField(to="secretarial.meetingagendamodel"),
                ),
                (
                    "minute_reading_acceptance_proposal",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="mr_acceptor",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "minute_reading_acceptance_proposal_support",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="mr_supporter",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "presidente",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="meet_president",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "secretary",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="meet_secretary",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "treasurer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="meet_treasurer",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Projeto de Ata",
                "verbose_name_plural": "Projeto de Ata",
            },
        ),
    ]