from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Habit
from .serializers import HabitSerializer, HabitCreateSerializer, HabitUpdateSerializer
from .permissions import IsOwner
from .pagination import HabitPagination


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

