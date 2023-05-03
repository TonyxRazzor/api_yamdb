import re
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

username_validator = UnicodeUsernameValidator()


def not_me_username_validator(value):
    """Запрещает использовать 'me' в качестве username."""
    if value.lower() == "me":
        raise ValidationError(
            "Вы не можете использовать 'me' в качестве username."
        )


def validate_username(value):
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(
            (f'Не допустимые символы <{value}> в нике.'),
            params={'value': value},
        )
