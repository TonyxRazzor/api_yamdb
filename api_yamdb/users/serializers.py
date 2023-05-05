from rest_framework import serializers

from users.models import CONF_CODE_MAX_LEN, EMAIL_MAX_LEN, USERNAME_MAX_LEN
from users.models import User
from users.validators import not_me_username_validator, username_validator


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserProfileSerializer(UserSerializer):
    """Сериализатор модели User для профиля пользователя."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ("role",)


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""

    username = serializers.CharField(
        max_length=USERNAME_MAX_LEN,
        required=True,
        validators=[not_me_username_validator, username_validator],
    )
    email = serializers.EmailField(
        max_length=EMAIL_MAX_LEN,
        required=True,
    )

    def validate_username(self, username):
        """Запрещает пользователям использовать символы в имени"""

        forbidden_chars = [r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$']
        for char in forbidden_chars:
            if char in username:
                raise serializers.ValidationError(
                    "Имя пользователя содержит запрещенные символы"
                )

        return username

    def validate_username(self, name):
        """Запрещает пользователям присваивать себе имя me"""

        if name == 'me':
            raise serializers.ValidationError(
                "Нельзя использовать me в качестве имени пользователя"
            )

        return name

    def validate(self, data):
        """Запрещает использовать повторные username и email."""

        username = data.get('username')
        email = data.get('email')
        if (
            User.objects.filter(username=username).exists()
            and User.objects.get(username=username).email != email
        ):
            raise serializers.ValidationError(
                "Пользователь с таким Email уже существует"
            )

        if (
            User.objects.filter(email=email).exists()
            and User.objects.get(email=email).username != username
        ):
            raise serializers.ValidationError(
                "Пользователь с таким username уже существует"
            )

        return data


class GetAuthTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(
        max_length=USERNAME_MAX_LEN,
        required=True,
        validators=[not_me_username_validator, username_validator],
    )
    confirmation_code = serializers.CharField(
        required=True, max_length=CONF_CODE_MAX_LEN
    )
