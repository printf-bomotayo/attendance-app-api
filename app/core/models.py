"""
Database models.
"""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


# Create your models here.

class UserManager(BaseUserManager):
    """Manager for users."""
    def create_user(self, email, password=None, **extra_fields):
        """Create save, and return a new user"""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the sytem."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  ## this is used to  assign user manager in django.

    USERNAME_FIELD = 'email' ## this is how to set the custom user model to use email as the authentication as against using Username which is the default that comes with Django user manager


class Attendance(models.Model):
    """Attendance object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='attendances'
        )
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=5, choices=[
        ('Late', 'Late'),
        ('Early', 'Early'),
    ])
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return f"{self.user.name}'s attendance on {self.date}"