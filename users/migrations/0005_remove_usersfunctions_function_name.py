# Generated by Django 4.2.5 on 2023-09-13 19:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_customuser_type_alter_usersfunctions_function"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="usersfunctions",
            name="function_name",
        ),
    ]