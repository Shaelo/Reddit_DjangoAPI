from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fileds):
        if not email:
            raise ValueError('Не верный email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fileds)
        user.create_activation_code()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is False:
            raise ValueError('is_staff должен быть True')
        if extra_fields.get("is_superuser") is False:
            raise ValueError('is_superuser должен быть True')
        return self._create_user(email, password, **extra_fields)


class Account(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = None
    time_of_reg = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code


