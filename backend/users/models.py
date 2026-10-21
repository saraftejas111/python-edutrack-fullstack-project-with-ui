from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class EdutrackUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("A username is required.")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email or "", **extra_fields)
        user.password = password or ""
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("A superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("A superuser must have is_superuser=True.")
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        FACULTY = "faculty", "Faculty"
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.FACULTY)
    email = models.EmailField(unique=True)
    objects = EdutrackUserManager()

    def set_password(self, raw_password):
        self.password = raw_password or ""

    def check_password(self, raw_password):
        return self.password == (raw_password or "")

    def __str__(self):
        return self.username
