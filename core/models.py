from decimal import Decimal

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

    MARK_CHOICES = (
        (DEPOSIT, 'Пополнение'),
        (WITHDRAW, 'Списание'),
    )

    user = models.ForeignKey(User, related_name='user_transactions', on_delete=models.PROTECT,
                             verbose_name='Пользователь')
    amount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма',
                                 validators=[MinValueValidator(Decimal('0.01'))])
    mark = models.CharField(choices=MARK_CHOICES, max_length=8, verbose_name='Тип транзакции')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано в')

    class Meta:
        verbose_name = 'транзакцию'
        verbose_name_plural = 'Транзакции'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} {"+" if self.mark == self.DEPOSIT else "-"}{self.amount}'

    @classmethod
    def get_total(cls, user):
        deposit = cls.objects.filter(user=user, mark='deposit').aggregate(s=Sum('amount'))['s'] or 0
        withdraw = cls.objects.filter(user=user, mark='withdraw').aggregate(s=Sum('amount'))['s'] or 0
        return deposit - withdraw
