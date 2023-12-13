import datetime
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('e-mail is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser is enable is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser is enable is_staff=True')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    image = models.ImageField(upload_to='users', blank=True, null=True)
    email = models.EmailField('e-mail', unique=True)
    phone = models.CharField('Phone', max_length=15, blank=True, null=True, unique=True)
    lat = models.CharField(max_length=20, null=True, blank=True)
    long = models.CharField(max_length=20, null=True, blank=True)
    expiration = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        um_dia = timezone.timedelta(days=1)
        self.expiration -= um_dia
        super().save(*args, **kwargs)

    def update_plain(self):
        self.expiration = datetime.datetime.now() + datetime.timedelta(days=31)
        self.save()

    def expiration_plain(self):
        return self.expiration < now()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    def __str__(self):
        return self.email

    objects = UserManager()
