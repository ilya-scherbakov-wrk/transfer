import binascii
import os
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum

from core.managers import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, verbose_name='Email')

    is_active = models.BooleanField(default=False, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')
    is_superuser = models.BooleanField(default=False, verbose_name='Суперюзер')

    objects = UserManager()

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано в')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено в')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}'


class UserTransaction(models.Model):
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'

    owner = models.ForeignKey(
        User,
        related_name='owner_transactions',
        on_delete=models.PROTECT,
        verbose_name='Отправитель',
        null=True,
        blank=True,
    )
    recipient = models.ForeignKey(
        User, related_name='recipient_transactions', on_delete=models.PROTECT, verbose_name='Получатель'
    )
    amount = models.DecimalField(
        decimal_places=2, max_digits=10, verbose_name='Сумма', validators=[MinValueValidator(Decimal('0.01'))]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано в')

    class Meta:
        verbose_name = 'транзакцию'
        verbose_name_plural = 'Транзакции'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.owner} - {self.amount} - {self.recipient}'

    @classmethod
    def get_total(cls, user):
        deposit = cls.objects.filter(recipient=user).aggregate(s=Sum('amount'))['s'] or 0
        withdraw = cls.objects.filter(owner=user).aggregate(s=Sum('amount'))['s'] or 0
        return deposit - withdraw

    def get_transaction_type(self, user):
        if user == self.owner:
            return self.WITHDRAW
        elif user == self.recipient:
            return self.DEPOSIT
        raise NotImplementedError


class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True, verbose_name='Ключ')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='auth_tokens', on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'токен'
        verbose_name_plural = 'REST-Токены'

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.get_random_token()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.key

    @classmethod
    def get_random_token(cls):
        return binascii.hexlify(os.urandom(20)).decode()
