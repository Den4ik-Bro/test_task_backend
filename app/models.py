from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Max


class Action(models.Model):
    CHOICES = [
        ('read', 'чтение'),
        ('create', 'создание'),
        ('update', 'изменение'),
        ('delete', 'удаление')
    ]
    session = models.ForeignKey('Session', on_delete=models.PROTECT, verbose_name='сессия')
    type = models.CharField(max_length=6, choices=CHOICES, verbose_name='тип')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    class Meta:
        verbose_name = 'Метод'
        verbose_name_plural = 'Методы'

    def __str__(self):
        return f'{self.type} {self.created_at}'


class Session(models.Model):
    account = models.ForeignKey('Account', on_delete=models.PROTECT, verbose_name='аккаунт')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    session_id = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'

    def __str__(self):
        return self.session_id


class Account(models.Model):
    number = models.PositiveIntegerField(verbose_name='номер')
    name = models.CharField(max_length=155, verbose_name='имя')

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    def __str__(self):
        return self.name


class Accrual(models.Model):
    date = models.DateField(verbose_name='дата')

    class Meta:
        verbose_name = 'Долг'
        verbose_name_plural = 'Долги'
        ordering = ['date']


class Payment(models.Model):
    date = models.DateField(verbose_name='дата')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['date']