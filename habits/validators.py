from django.core.exceptions import ValidationError


# Правило 1: исключить одновременный выбор связанной привычки и указания вознаграждения
def validate_linked_habit_and_reward(habit):
    """Нельзя одновременно указать связанную привычку и вознаграждение."""
    if habit.linked_habit and habit.reward:
        raise ValidationError(
            'Нельзя одновременно указать связанную привычку и вознаграждение. '
            'Выберите что-то одно.'
        )


# Правило 2: время выполнения не больше 120 секунд
def validate_duration(value):
    """Время выполнения привычки не должно превышать 120 секунд."""
    if value > 120:
        raise ValidationError(
            'Время выполнения привычки не должно превышать 120 секунд.'
        )


# Правило 3: в связанные привычки могут попадать только приятные привычки
def validate_linked_habit_is_pleasant(habit):
    """Связанная привычка должна быть приятной."""
    if habit.linked_habit and not habit.linked_habit.is_pleasant:
        raise ValidationError(
            'Связанная привычка должна иметь признак приятной привычки.'
        )


# Правило 4: у приятной привычки не может быть вознаграждения или связанной привычки
def validate_pleasant_habit(habit):
    """У приятной привычки не может быть вознаграждения или связанной привычки."""
    if habit.is_pleasant:
        if habit.reward:
            raise ValidationError(
                'У приятной привычки не может быть вознаграждения.'
            )
        if habit.linked_habit:
            raise ValidationError(
                'У приятной привычки не может быть связанной привычки.'
            )


# Правило 5: периодичность от 1 до 7 дней
def validate_periodicity(value):
    """Нельзя выполнять привычку реже, чем раз в 7 дней."""
    if value < 1 or value > 7:
        raise ValidationError(
            'Периодичность выполнения привычки должна быть от 1 до 7 дней.'
        )


# Общий валидатор модели, вызывающий все правила
def validate_habit(habit):
    """Полная валидация модели Habit."""
    validate_linked_habit_and_reward(habit)
    validate_linked_habit_is_pleasant(habit)
    validate_pleasant_habit(habit)
    # validate_duration и validate_periodicity вызываются как валидаторы полей
