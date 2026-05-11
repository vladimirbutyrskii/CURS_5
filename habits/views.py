from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from .models import Habit, TelegramUser
from .serializers import HabitSerializer, HabitCreateSerializer, HabitUpdateSerializer
from .permissions import IsOwner
from .pagination import HabitPagination

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import (
    HabitSerializer,
    HabitCreateSerializer,
    HabitUpdateSerializer,
    TelegramUserSerializer,
)


class HabitViewSet(viewsets.ModelViewSet):
    """CRUD для привычек текущего пользователя."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = HabitPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return HabitCreateSerializer
        elif self.action in ('update', 'partial_update'):
            return HabitUpdateSerializer
        return HabitSerializer

    def get_queryset(self):
        """Только привычки текущего пользователя."""
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Подстановка текущего пользователя при создании."""
        serializer.save(user=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    """Список публичных привычек (только чтение)."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        """Только публичные привычки, исключая привычки текущего пользователя."""
        return Habit.objects.filter(is_public=True).exclude(user=self.request.user)


class TelegramLinkView(generics.CreateAPIView):
    """Привязка Telegram-аккаунта к пользователю."""

    serializer_class = TelegramUserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        chat_id = request.data.get('chat_id')
        if not chat_id:
            return Response(
                {'error': 'chat_id обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создание или обновление привязки
        telegram_user, created = TelegramUser.objects.update_or_create(
            user=request.user,
            defaults={'chat_id': chat_id, 'is_active': True}
        )

        return Response(
            TelegramUserSerializer(telegram_user).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
