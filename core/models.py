from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """Define UserManager model."""

    def create_user(self, email, password=None):
        """Create a new user."""
        if not email:
            raise ValueError("Email needed.")
        if not password:
            raise ValueError("Password needed.")
        user = self.model(
            email=self.normalize_email(email)
                              )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create a new superuser."""
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """Define User model."""

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        """Represent the model in admin interface."""
        return self.email

    def has_perm(self, perm, obj=None):
        """Check if user have a specific permission."""
        return True

    def has_module_perms(self, app_label):
        """Check if the user have permissions to view the app."""
        return True

    @property
    def is_staff(self):
        """User is admin."""
        return self.is_admin
