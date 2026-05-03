from django.db import models
from django.conf import settings


class Habit(models.Model):
    """Модель привычки."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )
    place = models.CharField(
        max_length=255,
        verbose_name='Место выполнения'
    )
    time = models.TimeField(
        verbose_name='Время выполнения'
    )
    action = models.CharField(
        max_length=255,
        verbose_name='Действие'
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки'
    )
    linked_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='linked_to',
        verbose_name='Связанная привычка'
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name='Периодичность (в днях)'
    )
    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Вознаграждение'
    )
    duration = models.PositiveIntegerField(
        default=120,
        verbose_name='Время на выполнение (в секундах)'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user}: {self.action} в {self.place} в {self.time}'

