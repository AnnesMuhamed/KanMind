from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Validates registration data and creates a new user account.
    """

    fullname = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']

        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {'required': True}
        }

    def validate_email(self, value):
        """Ensures the email address is not already registered."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists.')
        return value

    def validate(self, attrs):
        """Ensures that both password fields match."""
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match.'}
            )
        return attrs

    def create(self, validated_data):
        """Creates the user with email as username and a hashed password."""
        first_name, last_name = self.split_fullname(validated_data['fullname'])
        user = User(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def split_fullname(self, fullname):
        """Splits a full name into first name and last name."""
        names = fullname.strip().split(' ', 1)
        if len(names) > 1:
            return names[0], names[1]
        return names[0], ''
