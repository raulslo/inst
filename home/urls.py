from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("home", PostView, basename='post')
router.register("comments", CommentsView, basename='commet')
router.register("likes", LikeViewSet,  basename='like')

app_name = "main_api"

urlpatterns = [

    path("", include(router.urls)),
]
