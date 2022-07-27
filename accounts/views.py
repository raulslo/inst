from rest_framework import status, generics

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db import IntegrityError

from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from accounts.models import User, UserProfile
from accounts.serializers import LoginSerializer, RegistrationSerializer, UserSerializer, ProfileSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication

from .permissions import UpdateOwnProfile, UpdateOwnUser

from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [UpdateOwnUser]
    serializer_class = UserSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["username"]
    search_fields = ["username"]


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          UpdateOwnProfile,)


    def perform_create(self, serializer):
        user = self.request.user
        try:
            serializer.save(user=user)
        except IntegrityError:
            raise ValidationError('Product with this Name and User already exists.')
