# Generated by Django 4.2.5 on 2023-10-16 13:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("secretarial", "0005_minuteprojectmodel"),
    ]

    operations = [
        migrations.RenameField(
            model_name="meetingminutemodel",
            old_name="presidente",
            new_name="president",
        ),
        migrations.RenameField(
            model_name="minuteprojectmodel",
            old_name="presidente",
            new_name="president",
        ),
    ]
