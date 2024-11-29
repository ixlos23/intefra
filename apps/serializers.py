from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from apps.models import Film, Genre


# Register serializer
class RegisterUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'date_of_birth', 'phone_number', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


# Login serializer
class LoginUserModelSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            raise ValidationError("Invalid email or password")

        if not user.check_password(password):
            raise ValidationError("Invalid email or password")

        attrs['user'] = user
        return attrs


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class FilmSerializer(ModelSerializer):
    genres = GenreSerializer(source='genre', many=True)

    class Meta:
        model = Film
        fields = '__all__'



