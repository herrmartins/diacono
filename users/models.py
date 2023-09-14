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
    phone_number = PhoneNumberField(blank=True, unique=True, region="BR")
    is_whatsapp = models.BooleanField(blank=True, default=False)
    about = models.TextField(blank=True)

    FUNCTION_CHOICES = (
        ("S", "SECRETÁRIO(A)"),
        ("T", "TESOUREIRO(A)"),
        ("A", "ADMINISTRADOR"),
        ("C", "CONGREGADO"),
        ("N", "NÃO ASSINALADO"),
    )

    class Types(models.TextChoices):
        REGULAR = "REGULAR", "Regular"
        STAFF = "STAFF", "Staff"
        ONLY_WORKER = "ONLY_WORKER", "Only Worker"

    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=Types.REGULAR
    )

    def get_absolute_url(self):
        return reverse_lazy(
            "users:user-profile", kwargs={"pk": str(self.id)},
            current_app="users"
        )


class RegularMemberManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super().get_queryset(*args, **kwargs).filter(
                type=CustomUser.Types.REGULAR)
        )


class StaffMemberManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            type=CustomUser.Types.STAFF)


class WorkerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(type=CustomUser.Types.ONLY_WORKER)
        )


class RegularMember(CustomUser):
    objects = RegularMemberManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = CustomUser.Types.REGULAR
        return super().save(*args, **kwargs)


class UsersFunctions(models.Model):
    member = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    function = models.CharField(
        max_length=1, choices=CustomUser.FUNCTION_CHOICES,
        blank=True, null=False
    )
    function_name = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Função"
        verbose_name_plural = "Funções"

    def __str__(self):
        return self.function


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


@receiver(post_save, sender=CustomUser)
def assing_role(sender, instance, created, **kwargs):
    if created:
        function = UsersFunctions(
            function="N", function_name="NÃO ASSINALADO", member_id=instance.id
        )
        function.save()
    else:
        print("Estou no else do pós-salvo...")
        reverse_lazy("core:home")
