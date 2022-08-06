from rest_framework.routers import DefaultRouter
from django.urls import include, path


from .views import UserViewSet, ProfileViewSet, FollowerView

app_name = "user"
router = DefaultRouter()
router.register("users", UserViewSet)
router.register("profiles", ProfileViewSet)
router.register("follow", FollowerView, basename="follow")


urlpatterns = [
    path("", include(router.urls)),
]
