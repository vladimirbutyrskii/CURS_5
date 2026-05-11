from rest_framework import serializers
from .models import Habit, TelegramUser


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения привычек."""

    class Meta:
        model = Habit
        fields = '__all__'


class HabitCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания привычки."""

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)

    def validate_linked_habit(self, value):
        """Проверка: связанная привычка должна быть приятной."""
        if value and not value.is_pleasant:
            raise serializers.ValidationError(
                'Связанная привычка должна иметь признак приятной.'
            )
        return value

    def validate(self, data):
        """Перекрёстная валидация на уровне сериализатора."""
        # Правило 1
        if data.get('linked_habit') and data.get('reward'):
            raise serializers.ValidationError(
                'Нельзя одновременно указать связанную привычку и вознаграждение.'
            )
        # Правило 4
        if data.get('is_pleasant'):
            if data.get('reward'):
                raise serializers.ValidationError(
                    'У приятной привычки не может быть вознаграждения.'
                )
            if data.get('linked_habit'):
                raise serializers.ValidationError(
                    'У приятной привычки не может быть связанной привычки.'
                )
        return data


class HabitUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления привычки."""

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)

    def validate_linked_habit(self, value):
        """Проверка: связанная привычка должна быть приятной."""
        if value and not value.is_pleasant:
            raise serializers.ValidationError(
                'Связанная привычка должна иметь признак приятной.'
            )
        return value

    def validate(self, data):
        """Перекрёстная валидация с учётом существующих данных (partial update)."""
        linked_habit = data.get('linked_habit', self.instance.linked_habit if self.instance else None)
        reward = data.get('reward', self.instance.reward if self.instance else None)
        is_pleasant = data.get('is_pleasant', self.instance.is_pleasant if self.instance else False)

        # Правило 1
        if linked_habit and reward:
            raise serializers.ValidationError(
                'Нельзя одновременно указать связанную привычку и вознаграждение.'
            )
        # Правило 4
        if is_pleasant:
            if reward:
                raise serializers.ValidationError(
                    'У приятной привычки не может быть вознаграждения.'
                )
            if linked_habit:
                raise serializers.ValidationError(
                    'У приятной привычки не может быть связанной привычки.'
                )
        return data


class TelegramUserSerializer(serializers.ModelSerializer):
    """Сериализатор для привязки Telegram."""

    class Meta:
        model = TelegramUser
        fields = ('id', 'user', 'chat_id', 'is_active')
        read_only_fields = ('user', 'is_active')
