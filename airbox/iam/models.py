from enum import Enum

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.db.models import EmailField, CharField, BooleanField, Model, DateTimeField, ForeignKey, CASCADE
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if not extra_fields.get('is_staff') or not extra_fields.get('is_superuser'):
            raise ValueError('invalid value')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = EmailField(_('email address'), unique=True)
    first_name = CharField(_('first name'), max_length=150)
    last_name = CharField(_('last name'), max_length=150)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()


class Organisation(Model):
    name = CharField(_('name'), max_length=150)
    created_at = DateTimeField(auto_now_add=True)


class Role(str, Enum):
    OWNER = 'owner'
    ADMIN = 'admin'
    EDITOR = 'editor'
    VIEWER = 'viewer'


class Member(Model):
    organisation = ForeignKey(Organisation, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    role = CharField(max_length=10, choices=[(role.value, role.name.title()) for role in Role], default=Role.VIEWER.value)
    joined_at = DateTimeField(auto_now_add=True)
