from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import UserViewSet,  ProfileViewSet


app_name = "accounts"
ROUTER = DefaultRouter()
ROUTER.register("users", UserViewSet)
ROUTER.register("profiles", ProfileViewSet)




urlpatterns = [
    path("", include(ROUTER.urls)),






]
