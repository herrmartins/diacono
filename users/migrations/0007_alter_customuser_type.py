# Generated by Django 4.2.5 on 2023-10-16 13:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_alter_customuser_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="type",
            field=models.CharField(
                choices=[
                    ("REGULAR", "Membro"),
                    ("EQUIPE", "Equipe"),
                    ("TRABALHADOR", "Contratado"),
                    ("CONGREGADO", "Congregado"),
                    ("USUARIO", "Usuário"),
                ],
                default="USUARIO",
                max_length=50,
                verbose_name="Type",
            ),
        ),
    ]