from rest_framework import status, generics

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from rest_framework.views import APIView

from user.permission import UpdateOwnProfile, UpdateOwnUser
from user.models import User, UserProfile, Follower
from user.serializers import (
    LoginSerializer,
    RegistrationSerializer,
    UserSerializer,
    ProfileSerializer,
    ListFollowerSerializer,
)

from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication

from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = UserSerializer
    permission_classes = [UpdateOwnUser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
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
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        UpdateOwnProfile,
    )


class FollowerView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Follower.objects.all()
    serializer_class = ListFollowerSerializer
