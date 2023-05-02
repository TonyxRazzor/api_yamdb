from rest_framework import serializers

from .constants import CONF_CODE_MAX_LEN, EMAIL_MAX_LEN, USERNAME_MAX_LEN
from .models import User
from .validators import not_me_username_validator, username_validator


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

    def validate(self, data):
        """Запрещает пользователям присваивать себе имя me
        и использовать повторные username и email."""

        if not User.objects.filter(
            username=data.get("username"), email=data.get("email")
        ).exists():
            if User.objects.filter(username=data.get("username")):
                raise serializers.ValidationError(
                    "Пользователь с таким username уже существует"
                )

            if User.objects.filter(email=data.get("email")):
                raise serializers.ValidationError(
                    "Пользователь с таким Email уже существует"
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
