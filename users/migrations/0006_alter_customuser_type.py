# Generated by Django 4.2.5 on 2023-10-14 13:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_remove_usersfunctions_member_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="type",
            field=models.CharField(
                choices=[
                    ("REGULAR", "Regular"),
                    ("EQUIPE", "Staff"),
                    ("TRABALHADOR", "Only Worker"),
                    ("CONGREGADO", "Congregated"),
                    ("USUÁRIO", "Usuário"),
                ],
                default="CONGREGADO",
                max_length=50,
                verbose_name="Type",
            ),
        ),
    ]
