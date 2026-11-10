from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from auth_app.api.serializers import RegistrationSerializer


class RegistrationView(APIView):
    """
    API view that handles new user registration.
    Allows unauthenticated access and returns an authentication token upon success.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Validates registration data and returns user details with a token."""
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(self._get_user_data(user))
        return Response(serializer.errors)

    def _get_user_data(self, user):
        """Helper method to generate token and response payload for a user."""
        token, created = Token.objects.get_or_create(user=user)
        return {
            'token': token.key,
            'username': user.username,
            'email': user.email
        }


class CustomLoginView(ObtainAuthToken):
    """
    Custom login view that authenticates users and returns
    their token along with user data.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Authenticates user credentials and returns token data."""
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response(self._get_user_data(user))
        return Response(serializer.errors)

    def _get_user_data(self, user):
        """Helper method to retrieve token and response payload for authenticated user."""
        token, created = Token.objects.get_or_create(user=user)
        return {
            'token': token.key,
            'username': user.username,
            'email': user.email
        }