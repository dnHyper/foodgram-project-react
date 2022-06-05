from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'

    USER_ROLE = (
        (USER, 'User role'),
        (ADMIN, 'Administrator role'),
    )

    email = models.EmailField(
        'Email',
        unique=True,
        error_messages={
            'unique': ('Такой email уже зарегистрирован'),
        }
    )

    first_name = models.TextField(
        'Имя',
        max_length=150,
        blank=True,
    )

    last_name = models.TextField(
        'Фамилия',
        max_length=150,
        blank=True,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField(
        'Пользовательская роль',
        max_length=15,
        choices=USER_ROLE,
        default=USER
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def __str__(self):
        return self.email


class Subscription(models.Model):
    """Модель пользовательских подписок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
    )

    class Meta:
        models.UniqueConstraint(
            fields=('user', 'following'),
            name='unique_subscription_user'
        )
