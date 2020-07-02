from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', "User table", False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User Table"""
    username = None
    email = models.EmailField('email address', unique=True)
    following = models.ManyToManyField(
        'self',
        through='FollowRelations',
        related_name='followers'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str(self):
        return self.email

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'


class FollowRelations(models.Model):
    RELATIONS_TYPES = (
        ('f', 'Follow'),
        ('b', 'Block'),
    )

    """follower"""
    from_relation = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower_relations',
        related_query_name='follower_relation'
    )
    """following"""
    to_relation = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following_relations',
        related_query_name='following_relation',
    )
    """relation type"""
    relation_type = models.CharField(
        max_length=1,
        choices=RELATIONS_TYPES,
        default='f'
    )
    followed_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = '팔로우'
        verbose_name_plural = f'{verbose_name} 목록'
        unique_together = [['from_relation', 'to_relation','relation_type']]