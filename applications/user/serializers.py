from django.contrib.auth import *
from rest_framework import serializers
from applications.user.models import Account
from applications.user.send_mail import send_activation_email, send_activation_code
from django.utils.crypto import get_random_string

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=6, write_only=True, required=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError('пароли не совпадают')
        attrs.pop('password_confirm')
        return attrs

    def validate_email(self, email):
        if not email.endswith('gmail.com'):
            raise serializers.ValidationError("email должен заканчиваться на 'gmail.com'")
        return email

    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        code = user.activation_code
        send_activation_email(code, user)

        return user

    class Meta:
        model = Account
        fields = ('email', 'password', 'password_confirm')


class LoginSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True)
        password = serializers.CharField(required=True)

        def validate_email(self, email):
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError('Пользователь не найден')
            return email

        def validate(self, attrs):
            email = attrs.get('email')
            password = attrs.get('password')

            if email and password:
                user = authenticate(username=email, password=password)

                if not user:
                    raise serializers.ValidationError('Не верный пароль или email')

                attrs['user'] = user
                return attrs


class RecoveryPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def new_password(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        new_password = get_random_string(8)
        user.set_password(new_password)
        send_activation_code(new_password, email)
        user.save()

        return user


class AccountSerializer(serializers.ModelSerializer):
    time_of_reg = serializers.DateTimeField(format=' %H:%M %d.%m.%Y', read_only=True)

    class Meta:
        model = Account
        fields = ('email', 'time_of_reg')
