from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import Group


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(
        blank=True, null=True, auto_now=False, auto_now_add=False
    )
    address = models.CharField(blank=True, max_length=255)
    # Não há validação, a não ser do próprio phonefield
    # Se colocar uma validação de telefone brasileiro,
    # se for estrangeiro, não vai dar.
    # Como, a princípio, não serão milhares de usuários,
    # vai dar certo.
    phone_number = PhoneNumberField(blank=True, unique=True, region="BR", null=True)
    is_whatsapp = models.BooleanField(blank=True, default=False)
    about = models.TextField(blank=True)
    married_to = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="spouse"
    )
    date_of_marriage = models.DateField(
        blank=True, null=True, auto_now=False, auto_now_add=False
    )
    is_pastor = models.BooleanField(blank=True, default=False)
    is_secretary = models.BooleanField(blank=True, default=False)
    is_treasurer = models.BooleanField(blank=True, default=False)

    class Types(models.TextChoices):
        # Um membro
        REGULAR = "REGULAR", "Membro"
        # Um membro com alguma função que utilize o sistema além do comum
        STAFF = "EQUIPE", "Equipe"
        # Caso se contrate um tesoureiro não membro
        ONLY_WORKER = "TRABALHADOR", "Contratado"

        CONGREGATED = "CONGREGADO", "Congregado"

        SIMPLE_USER = "USUARIO", "Usuário"

    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=Types.SIMPLE_USER
    )

    def get_absolute_url(self):
        return reverse_lazy(
            "users:user-profile", kwargs={"pk": str(self.id)}, current_app="users"
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


@receiver(pre_save, sender=CustomUser)
def update_user_type(sender, instance, **kwargs):
    congregated_group = Group.objects.get(name='congregated')
    regular_group = Group.objects.get(name='members')
    secretarial_group = Group.objects.get(name='secretarial')
    treasury_group = Group.objects.get(name='treasurer')
    pastor_group = Group.objects.get(name='pastor')

    instance.groups.clear()

    print("Instance type:", instance.type)
    print("Is pastor:", instance.is_pastor)
    print("Is secretary:", instance.is_secretary)
    print("Is treasurer:", instance.is_treasurer)

    if instance.type in [CustomUser.Types.CONGREGATED, CustomUser.Types.SIMPLE_USER]:
        instance.error_message = "Congregado não pode ter funções..."
        instance.is_pastor = False
        instance.is_secretary = False
        instance.is_treasurer = False
        instance.groups.add(congregated_group)
    else:
        if instance.type == CustomUser.Types.REGULAR:
            instance.groups.add(regular_group)

        if instance.is_pastor:
            print("Assigning to pastor group")
            instance.groups.add(pastor_group)
        if instance.is_secretary:
            print("Assigning to secretarial group")
            instance.groups.add(secretarial_group)
        if instance.is_treasurer:
            print("Assigning to treasurer group")
            instance.groups.add(treasury_group)

        # Check if the user has any function
        has_any_function = (
            instance.is_pastor or instance.is_secretary or instance.is_treasurer
        )
        print("Has any function:", has_any_function)
        if has_any_function:
            instance.type = CustomUser.Types.STAFF
            instance.is_staff = True
        else:
            instance.type = CustomUser.Types.REGULAR
            instance.is_staff = False
            instance.groups.add(regular_group)
