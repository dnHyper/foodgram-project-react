from rest_framework import serializers

from users.models import User


class UserShowSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода пользователя/списка пользователей."""
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=150, required=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )


class UserSerializer(serializers.ModelSerializer):
    """Основной кастомный сериализатор пользователя с доп. полями."""
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=150, required=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(
        min_length=4,
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'role'
        )

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError(
                "Пользователь с такой почтой уже зарегистрирован."
            )

        return data

    def validate_username(self, data):
        if User.objects.filter(username=data).exists():
            raise serializers.ValidationError(
                "Пользователь с таким именем уже существует."
            )

        return data

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации."""
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    banned_names = ('me', 'admin', 'ADMIN', 'administrator', 'moderator')

    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate_username(self, data):
        if data in self.banned_names:
            raise serializers.ValidationError(
                "Нельзя использовать такое имя."
            )

        if User.objects.filter(username=data).exists():
            raise serializers.ValidationError(
                "Пользователь с таким именем уже существует."
            )

        return data

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError(
                "Пользователь с такой почтой уже зарегистрирован."
            )

        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена."""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=24)
