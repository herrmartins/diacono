# Generated by Django 4.2.5 on 2023-10-16 14:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_alter_customuser_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usersfunctions",
            name="function",
            field=models.CharField(
                choices=[
                    ("N", "Não assinalado"),
                    ("P", "Pastor"),
                    ("M", "Moderador"),
                    ("S", "Secretário"),
                    ("T", "Tesoureiro"),
                ],
                max_length=1,
            ),
        ),
    ]
