from django.contrib import admin
from .models import Habit, TelegramUser


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'place', 'time', 'is_pleasant', 'is_public', 'periodicity')
    list_filter = ('is_pleasant', 'is_public', 'periodicity')
    search_fields = ('action', 'place', 'user__email')


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'chat_id', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('user__email', 'chat_id')
