# Generated by Django 3.2.14 on 2023-08-29 15:31

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активен')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Персонал')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Суперюзер')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано в')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено в')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'пользователя',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='UserTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Сумма')),
                ('mark', models.CharField(choices=[('deposit', 'Пополнение'), ('withdraw', 'Списание')], max_length=8, verbose_name='Тип транзакции')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано в')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_transactions', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'транзакцию',
                'verbose_name_plural': 'Транзакции',
                'ordering': ['-created_at'],
            },
        ),
    ]
