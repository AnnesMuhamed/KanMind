from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.api.serializers import RegistrationSerializer


def _get_user_data(user):
    """Returns the token and the user details for the auth response."""
    token, created = Token.objects.get_or_create(user=user)
    return {
        'token': token.key,
        'fullname': user.get_full_name(),
        'email': user.email,
        'user_id': user.id,
    }


class RegistrationView(APIView):
    """Registers a new user and returns the token with user details."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Validates the registration data and creates the user."""
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = _get_user_data(user)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(ObtainAuthToken):
    """Logs a user in by email and returns the token with user details."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Checks email and password and returns the user details."""
        data = {
            'username': request.data.get('email'),
            'password': request.data.get('password'),
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response(_get_user_data(user), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
