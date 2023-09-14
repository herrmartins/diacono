from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


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
    phone_number = PhoneNumberField(blank=True, unique=True, region="BR")
    is_whatsapp = models.BooleanField(blank=True, default=False)
    about = models.TextField(blank=True)

    class Types(models.TextChoices):
        # Um membro
        REGULAR = "REGULAR", "Regular"
        # Um membro com alguma função que utilize o sistema além do comum
        STAFF = "STAFF", "Staff"
        # Caso se contrate um tesoureiro não membro
        ONLY_WORKER = "ONLY_WORKER", "Only Worker"

        CONGREGATED = "CONGREGATED", "Congregated"

    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=Types.REGULAR
    )

    def get_absolute_url(self):
        return reverse_lazy(
            "users:user-profile", kwargs={"pk": str(self.id)},
            current_app="users"
        )


class UsersFunctions(models.Model):
    class Types(models.TextChoices):
        NOT_ASSIGNED = "N", "Não assinalado"
        PASTOR = "P", "Pastor"
        SECRETARY = "S", "Secretário"
        TREASURER = "T", "Tesoureiro"

    member = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    function = models.CharField(
        max_length=1, choices=Types.choices, blank=True, null=False
    )

    class Meta:
        verbose_name = "Função"
        verbose_name_plural = "Funções"

    def __str__(self):
        return self.function


class RegularMemberManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super().get_queryset(*args, **kwargs).filter(
                type=CustomUser.Types.REGULAR
            )
        )


class StaffMemberManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            type=CustomUser.Types.STAFF
        )


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


@receiver(post_save, sender=CustomUser)
def assing_role(sender, instance, created, **kwargs):
    if created:
        function = UsersFunctions(
            function="N", function_name="NÃO ASSINALADO", member_id=instance.id
        )
        function.save()
    else:
        print("Tou aqui no else do post_save custumuser")
        reverse_lazy("core:home")
