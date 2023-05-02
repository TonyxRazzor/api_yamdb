from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    """Валидатор года для произведений."""

    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{value} не может быть больше {now}'
        )
