from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        # create new user by using create_user method from the User class
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # validating email and password - check if it's correct and compare to ones in database
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise exceptions if password or email is not provided

        if password is None:
            raise serializers.ValidationError(
                'Password field is requried to log in')
        if email is None:
            raise serializers.ValidationError('E-mail is required to log in')

        # capture the user
        # check if 'User' is_active - banned or deactivated
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found')

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been banned or deactivated')

        # return data about the user - data that's used in create and update methods on User class.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    # Used to hanlde serialization and deserialization of User objects
    # - password must be at least 8 chars long
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token',)

        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        # updating data - PUT/EDIT
        # remove password field from validated_data

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # for remaining keys in validated_data set them to the current 'User' instance
            setattr(instance, key, value)

        if password is not None:
            # '.set_password()' - Django built in security functionlity for password
            instance.set_password(password)

        instance.save()

        return instance
