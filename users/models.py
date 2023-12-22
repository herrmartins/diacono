from django.contrib.auth.models import AbstractUser

from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import pre_save
from django.dispatch import receiver


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
    functions = models.ManyToManyField(
        "UsersFunctions", related_name="user_roles", blank=True
    )
    married_to = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="spouse"
    )
    date_of_marriage = models.DateField(
        blank=True, null=True, auto_now=False, auto_now_add=False
    )

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


class UsersFunctions(models.Model):
    class Types(models.TextChoices):
        NOT_ASSIGNED = "N", "Não assinalado"
        PASTOR = "P", "Pastor"
        MODERATOR = "M", "Moderador"
        SECRETARY = "S", "Secretário"
        TREASURER = "T", "Tesoureiro"

    function = models.CharField(max_length=1, choices=Types.choices)

    class Meta:
        verbose_name = "Função"
        verbose_name_plural = "Funções"

    def __str__(self):
        return self.get_function_display()


class RegularMemberManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.REGULAR)
        )


class StaffMemberManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Types.STAFF)


class OnlyWorkerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(type=CustomUser.Types.ONLY_WORKER)
        )


class CongregatedManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(type=CustomUser.Types.CONGREGATED)
        )


class RegularMember(CustomUser):
    objects = RegularMemberManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = CustomUser.Types.REGULAR
        return super().save(*args, **kwargs)


class StaffMember(CustomUser):
    base_type = CustomUser.Types.STAFF
    objects = StaffMemberManager()

    @property
    def set_funcion(self):
        return self.usersfunctions()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = CustomUser.Types.STAFF
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class OnlyWorker(CustomUser):
    objects = OnlyWorkerManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = CustomUser.Types.REGULAR
        return super().save(*args, **kwargs)


class Congregated(CustomUser):
    objects = CongregatedManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = CustomUser.Types.REGULAR
        return super().save(*args, **kwargs)


@receiver(pre_save, sender=CustomUser)
def update_user_type(sender, instance, **kwargs):
    # Check if the user is of type REGULAR
    if instance.type == CustomUser.Types.REGULAR:
        # Check if the user has functions
        if instance.functions.exists():
            # Upgrade the user to STAFF
            instance.type = CustomUser.Types.STAFF
            instance.save()
