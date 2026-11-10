from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for handling user registration, validating password matching,
    duplicate emails, and securely creating new user accounts with hashed passwords.
    """
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self):
        """
        Validates that both passwords match, creates a new user instance,
        hashes the password securely, and saves the account to the database.
        """
        pw = self.validated_data['password']
        repeated_password = self.validated_data['repeated_password']

        if pw != repeated_password:
            raise serializers.ValidationError({
                'password': 'Passwords must match.'
            })  

        account = User(
             email=self.validated_data['email'],
             username=self.validated_data['username']
        )      

        account.set_password(pw)
        account.save()

        return account

    def validate_email(self, value):
        """
        Validates that the provided email address is unique
        and does not already exist in the database.
        """
        if User.objects.filter(email=value).exists():
              raise serializers.ValidationError(
                   'Email already exists.'
              )
        return value