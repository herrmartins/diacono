# Generated by Django 4.2.5 on 2023-10-17 20:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("secretarial", "0009_meetingminutemodel_number_of_attendees"),
    ]

    operations = [
        migrations.RenameField(
            model_name="minuteprojectmodel",
            old_name="number_of_atendees",
            new_name="number_of_attendees",
        ),
    ]
