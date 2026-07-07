from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user with name, email, and password."""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                "message": "User registered successfully.",
                "user": {
                    "id": user.id,
                    "name": user.first_name,
                    "email": user.email,
                },
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(
        {"errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Log in a user and return JWT tokens."""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Authenticate using email as username
        user = authenticate(username=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login successful.",
                    "tokens": {
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    },
                    "user": {
                        "id": user.id,
                        "name": user.first_name,
                        "email": user.email,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid email or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    return Response(
        {"errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )
